import logging
import time
from cv2 import (
    findContours,
    contourArea,
    threshold,
    morphologyEx,
    INTER_LINEAR,
    MORPH_CLOSE,
    THRESH_BINARY,
    RETR_TREE,
    CHAIN_APPROX_SIMPLE,
    connectedComponents,
    minEnclosingCircle, 
    minAreaRect,
    THRESH_TOZERO,
    circle
    )
import numpy as np
from fractions import Fraction
from decimal import Decimal
from math import pi
from typing import TYPE_CHECKING

    # from src.vision.image_frame import ImageFrame
# from src.vision.image_tools import ImageSize

LOGGER = logging.getLogger(__name__)

ECCENTRICITY_CRITERIA = 0.7
IS_CONTOUR_EMPTY_CRITERIA = 0.4

R_TH_100um = 44/2048
R_TH_200um = 80/2048
R_TH = R_TH_200um
ALGO_TIMEOUT_IN_SECONDS = 0.5
import cv2

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
    

def find_image_center(in_image):
    size = np.shape(in_image)
    h, w = size[0], size[1]
    center = (int(h / 2), int(w / 2))
    return center


def get_laser_spot_blob(image_frame: np.ndarray):
    height = 512
    width = int(height * image_frame.aspect_ratio())
    input_image = get_frame_resized(image_frame, size = size)
    blob, rec_time, found, binary_image = find_laser_spot_main_call(input_image)
    return blob

def get_frame_resized(image, size=(647, 647)) -> np.ndarray:
    image_to_resize = image
    if size[0] == size[1]:
        image_to_resize = ImageTools.square_image(self.frame)
        if image_to_resize.shape == (0,0):
            return image

    resized_image = cv2.resize(frame, size)
    return resized_image


def square_image(in_img:np.ndarray) -> np.ndarray:
    size = np.shape(in_img)[:2]
    center = (int(size[0]/2),int(size[1]/2))
    newSize = min(size)
    if newSize%2!=0:
        newSize = newSize-1
    newSize = int(newSize/2)
    return in_img[center[0]-newSize:center[0]+newSize,center[1]-newSize:center[1]+newSize]



def format_blob(in_image, formatted_image, laser_spot_parameter):
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


def find_laser_spot_main_call(in_image: np.ndarray):
    formatted_image = format_image(in_image)

    time_start = time.time()

    found, rec_time, c_h, c_w, radius, binary_image = find_laser_spot_recursive(
        formatted_image, 0.95, time_start, 0)
    blob = format_blob(in_image, formatted_image, [c_h, c_w, radius, found])

    time_elapsed = (time.time() - time_start)

    laser_found = "Laser found" if found else "Laser NOT found"

    return blob


def find_laser_spot_recursive(input_image, thr, start_time, rec_time):
    rec_time = rec_time + 1
    red_channel = input_image[:,:,2]
    green_channel = input_image[:,:,1]

    in_img_size = green_channel.shape

    binary_image = binarize_laser_image(input_image, thr)

    cc = ConnectedComponents()
    cc.get_properties_connected_component(binary_image)

    current_time = time.time() - start_time
    if current_time > ALGO_TIMEOUT_IN_SECONDS:
        return False, rec_time, 0, 0, 0, binary_image

    if thr < 0.5:
        return False, rec_time, 0, 0, 0, binary_image

    t = time.time()
    list_idx = np.flip(np.argsort(cc.area_list), 0)

    if len(cc.area_list) > 0:
        area_number = len(cc.area_list)

        for idx in list_idx:
            circle_centroid = cc.centroid_list[idx]
            blue_channel = input_image[:,:,0]
            red_channel_pixel = red_channel[int(circle_centroid[1]), int(circle_centroid[0])]
            blue_channel_pixel = blue_channel[int(circle_centroid[1]), int(circle_centroid[0])]
            
            is_red = red_channel_pixel >= blue_channel_pixel

            if is_red:
                circle_radius = cc.radius_list[idx]

                if int(circle_radius) > int(0.80 * R_TH * in_img_size[0]) and int(circle_radius) <= int(1.45 * R_TH * in_img_size[0]):
                    minor_axis = np.min([cc.minor_axis_list[idx], cc.major_axis_list[idx]])
                    major_axis = np.max([cc.minor_axis_list[idx], cc.major_axis_list[idx]])
                    is_a_circle = minor_axis/major_axis > ECCENTRICITY_CRITERIA
                    if is_a_circle:
                        area = cc.area_list[idx]
                        cntr = cc.contour[idx]

                        mask = np.zeros(input_image.shape[:2], np.uint8)
                        cv2.drawContours(mask,[cntr],0,1,-1)
                        binary_image = binary_image/255
                        overlap_blob_binary_image = mask*binary_image
                        pixel_prop_with_one_value_in_blob = np.sum(overlap_blob_binary_image)/area
                        if pixel_prop_with_one_value_in_blob >= IS_CONTOUR_EMPTY_CRITERIA:
                            return True, rec_time, float(circle_centroid[1]), float(
                                circle_centroid[0]), float(circle_radius), binary_image
    th = thr - 0.1
    return find_laser_spot_recursive(input_image, th, start_time, rec_time)


def binarize_laser_image(input_image, thresh):
    gray_image = cv2.cvtColor(input_image, cv2.COLOR_BGR2GRAY)
    max = np.max(gray_image)

    retval, binary_image = threshold(
        gray_image, int(max * thresh)+3, 255, THRESH_TOZERO)
    retval, binary_image = threshold(
        binary_image, int(max * thresh)-3, 255, THRESH_BINARY)

    binary_image = morphologyEx(
        binary_image, MORPH_CLOSE, kernel=np.ones((6, 6)))
    return binary_image


if __name__ == "__main__":
    import matplotlib.pyplot as plt
    import os
    path = os.path.abspath(os.getcwd())
    # image_path = os.path.join(path, 'eye5-92-3097_laser.jpeg')
    image_path = os.path.join(path, 'eye1-39-2521_laser.jpeg')
    image = cv2.imread(image_path)
    image_size = image.shape

    #the find_laser_spot function takes a bgr image as input, won't work if you give rgb image
    blob = find_laser_spot_main_call(image)
    center = (int(blob['center']['x']*image_size[1]), int(blob['center']['y']*image_size[0]))
    radius = int(blob['radius']*image_size[0])
    cv2.circle(image, center, radius, (255,0,0), 2)
    print(center)

    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    plt.imshow(image_rgb)
    plt.show()