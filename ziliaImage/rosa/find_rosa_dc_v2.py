import logging
import time
from cv2 import (
    findContours,
    contourArea,
    threshold,
    THRESH_BINARY,
    RETR_TREE,
    CHAIN_APPROX_SIMPLE,
    minEnclosingCircle, 
    minAreaRect,
    THRESH_TOZERO,
    circle,
    COLOR_BGR2GRAY,
    cvtColor,
    morphologyEx,
    MORPH_CLOSE
    )
import cv2
from fractions import Fraction
from decimal import Decimal
import numpy as np
from math import pi
from typing import TYPE_CHECKING

LOGGER = logging.getLogger(__name__)

ECCENTRICITY_CRITERIA = 0.7
IS_CONTOUR_EMPTY_CRITERIA = 0.4

R_25_um = 10/2048
R_75_um = 30/2048

R_TH_100um = 44/2048
R_TH_200um = 80/2048
R_300_um = 100/2048

R_TH = R_TH_200um
ALGO_TIMEOUT_IN_SECONDS = 0.05


def extract_gray_map_from_red_channel(image):
    b = image[:,:,0]
    r = image[:,:,2]
    red_channel = r >= b

    gray_level_img = cvtColor(image, COLOR_BGR2GRAY)

    out_img = red_channel*gray_level_img

    out_img = out_img.astype(np.uint8)
    return out_img

class ConnectedComponents:
    def __init__(self):
        self.area_list = []
        self.centroid_list = []
        self.minor_axis_list = []
        self.major_axis_list = []
        self.radius_list = []
        self.contour = []

    def get_properties_connected_component(self, binary_image):
        try:
            _, contours, _ = findContours(
                binary_image, RETR_TREE, CHAIN_APPROX_SIMPLE)
        except:
            contours, _ = findContours(
                binary_image, RETR_TREE, CHAIN_APPROX_SIMPLE)
        
        for cntr in contours:
            if len(cntr) > 4:
                area = contourArea(cntr)
                if int(area) > 15:
                    
                    center, radius = minEnclosingCircle(cntr)
                    
                    (_,_), (major_axis, minor_axis), _ = minAreaRect(cntr)

                    
                    self.centroid_list.append(center)
                    self.radius_list.append(radius)
                    area = pi * radius * radius
                    self.area_list.append(area)
                    self.major_axis_list.append(minor_axis / 2)
                    self.minor_axis_list.append(major_axis / 2)
                    self.contour.append(cntr)
    
def analyze_binary_image_for_rosa(binary_image):

    in_img_size = binary_image.shape

    cc = ConnectedComponents()
    cc.get_properties_connected_component(binary_image)
    if len(cc.area_list) >= 15:
        return False, 0, 0, 0

    t = time.time()
    list_idx = np.flip(np.argsort(cc.area_list), 0)

    if len(cc.area_list) > 0:
        area_number = len(cc.area_list)
        if area_number > 1:
            LOGGER.debug("Multiple areas:" + str(area_number))
        for idx in list_idx:
            circle_centroid = cc.centroid_list[idx]
            circle_radius = cc.radius_list[idx]
            if int(circle_radius) > int(R_75_um * in_img_size[0]) and int(circle_radius) <= int(R_300_um * in_img_size[0]):
                minor_axis = np.min([cc.minor_axis_list[idx], cc.major_axis_list[idx]])
                major_axis = np.max([cc.minor_axis_list[idx], cc.major_axis_list[idx]])
                is_a_circle = minor_axis/major_axis > ECCENTRICITY_CRITERIA
                if is_a_circle:
                    return True, float(circle_centroid[1]), float(circle_centroid[0]), float(circle_radius)
    return False, 0, 0, 0
    

def format_blob(in_image, laser_spot_parameter):
    captor_ratio = 1.18
    c_h, c_w, radius, found = laser_spot_parameter
    h, w = in_image.shape[0], in_image.shape[1]

    rectangle_height = min(h,w)
    rectangle_width = max(h,w)

    r, c = c_w, c_h

    radius = int(radius)
    blob = {
        'center': {
            "x": r / rectangle_width,
            "y": c / rectangle_height,
            "rx": r,
            "ry": c},
        'radius': float(
            Fraction(
                Fraction(
                    Decimal(radius)),
                h)),
        'rradius': radius,
        'found': found}
    return blob


def format_image(in_image: np.ndarray) -> np.ndarray:
    out_image = np.array(in_image, dtype=np.uint8)
    return out_image

def fine_tune_rosa_detection(red_channel, c_h, c_w, radius):
    h, w = np.shape(red_channel)
    c_h, c_w = int(c_h), int(c_w)

    c_h_orig, c_w_orig = int(c_h), int(c_w)
    original_radius = int(radius)

    h_crop = h/8
    w_crop = w/8
    h_min = np.amax([int(c_h-h_crop), 0])
    h_max = np.amin([int(c_h+h_crop), h])
    
    w_min = np.amax([int(c_w-w_crop), 0])
    w_max = np.amin([int(c_w+w_crop), h])

    crop_img = red_channel[h_min:h_max, w_min:w_max]

    new_img = np.zeros((h,w))
    new_img[h_min:h_max, w_min:w_max] = crop_img
    perc = int(np.max([np.percentile(crop_img, 95) - 1, 0]))

    in_img_size = red_channel.shape
    if int(perc) == 0:
        return c_h, c_w, original_radius
 
    else:
        _, binary_image = threshold(new_img, int(perc), 255, THRESH_BINARY)

        binary_image = binary_image.astype(np.uint8)
        found, c_h, c_w, radius = analyze_binary_image_for_rosa(binary_image)
        if found:
            return c_h, c_w, radius
        else:
            return c_h_orig, c_w_orig, original_radius
    return c_h_orig, c_w_orig, original_radius


def find_laser_spot_main_call(in_image: np.ndarray):
    formatted_image = format_image(in_image)

    time_start = time.time()
    red_channel = extract_gray_map_from_red_channel(formatted_image)
    max_value_red_channel = np.max(red_channel)
 
    found, rec_time, c_h, c_w, radius = find_laser_spot_recursive(
        red_channel, 0.95, max_value_red_channel, time_start, 0)

    if found:
        c_h, c_w, fine_tuned_radius = fine_tune_rosa_detection(red_channel, c_h, c_w, radius)
        radius = fine_tuned_radius

    blob = format_blob(in_image, [c_h, c_w, radius, found])
    time_elapsed = (time.time() - time_start)

    laser_found = "Laser found" if found else "Laser NOT found"

    LOGGER.warning(
        str.format(
            "{0}. Took {1}. Recursive count {2}",
            laser_found,
            str(time_elapsed),
            str(rec_time)))

    return blob, rec_time, found


def find_laser_spot_recursive(red_channel, thr, max_value, start_time, rec_time):
    rec_time = rec_time + 1

    binary_image = binarize_laser_image(red_channel, thr, max_value)

    current_time = time.time() - start_time
    if current_time > ALGO_TIMEOUT_IN_SECONDS:
        LOGGER.warning(
            str.format(
                "Laser spot not found - too long: Took {0} for {1} iteration.",
                str(current_time),
                rec_time))
        return False, rec_time, 0, 0, 0

    if thr < 0.4:
        LOGGER.debug(
            str.format(
                "Laser spot not found after {0} iteration in {1}",
                rec_time,
                str(current_time)))
        return False, rec_time, 0, 0, 0

    found, c_h, c_w, circle_radius = analyze_binary_image_for_rosa(binary_image)
    if found:
        return True, rec_time, c_h, c_w, circle_radius
    
    else:
        th = thr - 0.1
        return find_laser_spot_recursive(red_channel, th, max_value, start_time, rec_time)


def binarize_laser_image(input_image, thresh, max_value):
    gray_image = input_image
    max = max_value

    half_range = 3
    retval, binary_image = threshold(
        gray_image, int(max * thresh)-half_range, 255, THRESH_TOZERO)
    retval, binary_image = threshold(
        binary_image, int(max * thresh)+half_range, 255, THRESH_BINARY)
    

    return binary_image


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import os
    path = os.path.abspath(os.getcwd())
    image_path = os.path.join(path, 'eye5-92-3097_laser.jpeg')
    # image_path = os.path.join(path, 'eye1-39-2521_laser.jpeg')
    image = cv2.imread(image_path)
    image_size = image.shape

    blob, rec_time, found = find_laser_spot_main_call(image)



    #the find_laser_spot function takes a bgr image as input, won't work if you give rgb image
    center = (int(blob['center']['x']*image_size[1]), int(blob['center']['y']*image_size[0]))
    radius = int(blob['radius']*image_size[0])
    cv2.circle(image, center, radius, (255,0,0), 2)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()