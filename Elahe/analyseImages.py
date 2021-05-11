"""
Has the following class:
- ConnectedComponents

This class has the following methods:
- __init__(self)
- getPropertiesConnectedComponent(self, binary_image)


Then this module has the following functions:
- extractGrayMapFromRedChannel(image)
- analyzeBinaryImageForRosa(binary_image)
- formatBlob(in_image, laser_spot_parameter)
- fineTuneRosaDetection(red_channel, c_h, c_w, radius)
- findLaserSpotMainCall(in_image: np.ndarray)
- findLaserSpotRecursive(red_channel, thr, max_value, start_time, rec_time)
- binarizeLaserImage(input_image, thresh, max_value)
- mainRosa(image_path)

WARNING:
-mainRosa is called in functions2.py!!!

"""

import logging
import time
# opencv python (cv2) is related to computer vision things
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
ALGO_TIMEOUT_IN_SECONDS = 0.5


class ConnectedComponents:
    def __init__(self):
        self.area_list = []
        self.centroid_list = []
        self.minor_axis_list = []
        self.major_axis_list = []
        self.radius_list = []
        self.contour = []

    def getPropertiesConnectedComponent(self, binary_image):
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


def extractGrayMapFromRedChannel(image):
    """
    Extract the red channel from an image.
    Input: image as a numpy array.
    Output: red channel of the image as a numpy array.
    """
    blue = image[:,:,0]
    red = image[:,:,2]
    red_channel = red >= blue

    # Convert image from colorful to gray scale
    gray_level_img = cvtColor(image, COLOR_BGR2GRAY)
    out_img = red_channel*gray_level_img

    formattedImage = out_image.astype(np.uint8)
    return formattedImage


def analyzeBinaryImageForRosa(binary_image):
    in_img_size = binary_image.shape

    cc = ConnectedComponents()
    cc.getPropertiesConnectedComponent(binary_image)
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


def formatBlob(in_image, laser_spot_parameter):
    """
    Format parameters of the blop and turn them into an organized dictionary.
    Input: in_image(image as a numpy array).
           laser_spot_parameter(an iterable object containing [circle height,
                            circle width, circle radius, True/False value
                            that tells if the spot was found or not]).
    Output: blob(a dictionary that contains all parameters of the blob:
                {"center":{
                        "x": horizontal position of the center of the blob.
                        "y": vertical position of the center of the blob.
                        "rx": horizontal radius of the blob.
                        "ry": vertical radius of the blob.
                        }
                "radius": radius of the smallest circle that surrounds the
                          blob.
                "rradius": rounded radius (is an integer)
                "found": True/False, tells if a spot was found or not.
                }
                )
    """
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
        'radius': float(Fraction(Fraction(Decimal(radius)), h)),
        'rradius': radius,
        'found': found}
    return blob


def fineTuneRosaDetection(red_channel, c_h, c_w, radius):
    """
    Fine tune the detection of the Rosa in an image.
    Input: red_channel(red channel of the image).
           c_h(the height of the circle).
           c_w(the width of the circle).
           radius(the radius of the circle).
    Output: 
    """
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
        found, c_h, c_w, radius = analyzeBinaryImageForRosa(binary_image)
        if found:
            return c_h, c_w, radius
        else:
            return c_h_orig, c_w_orig, original_radius
    return c_h_orig, c_w_orig, original_radius


def findLaserSpotMainCall(in_image: np.ndarray):
    """
    Try to find the laser spot in the image.
    Calls a recursive algorithm to do so.
    Input: image as a 3D numpy array.
    Output: blob(output of the formatBlop function, which is a dictionary
                containing parameters of the blob).
            rec_time(number of times the recusive algorithm was called).
            found(True or False, says if laser spot was found or not).
    """

    formatted_image = in_image.astype(np.uint8)

    time_start = time.time()
    red_channel = extractGrayMapFromRedChannel(formatted_image)
    max_value_red_channel = np.max(red_channel)
 
    found, rec_time, c_h, c_w, radius = findLaserSpotRecursive(
        red_channel, 0.95, max_value_red_channel, time_start, 0)

    if found:
        c_h, c_w, fine_tuned_radius = fineTuneRosaDetection(red_channel, c_h, c_w, radius)
        radius = fine_tuned_radius

    blob = formatBlob(in_image, [c_h, c_w, radius, found])
    time_elapsed = (time.time() - time_start)

    laser_found = "Laser found" if found else "Laser NOT found"

    LOGGER.warning(
            f"{laser_found}. Took {str(time_elapsed)}. Recursive count {str(rec_time)}")

    return blob, rec_time, found


def findLaserSpotRecursive(red_channel, thr, max_value, start_time, rec_time):
    """
    Use a recursive algorithm to try to find the laser spot in the image.
    Input: red_channel(red channel of the image),
           thr(the set threshold),
           max_value(maximum light intensity of red channel),
           start_time,
           rec_time(number of times the recursive algorithm got executed so
              far).
    Output: Found(True or False, says if laser spot was found or not),
            rec_time(number of times the recursive algorithm was ececuted),
            c_h(0 if "found" is False, circle height if found is True),
            c_w(0 if "found" is False, circle width if found is True),
            radius(0 if found is False, circle radius if found is True).
    """
    rec_time = rec_time + 1

    binary_image = binarizeLaserImage(red_channel, thr, max_value)

    current_time = time.time() - start_time
    if current_time > ALGO_TIMEOUT_IN_SECONDS:
        LOGGER.warning(
            f"Laser spot not found - too long: Took {str(current_time)} for {rec_time} iteration."
            )
        return False, rec_time, 0, 0, 0

    if thr < 0.4:
        LOGGER.debug(f"Laser spot not found after {rec_time} iteration in {str(current_time)}")
        return False, rec_time, 0, 0, 0
    found, c_h, c_w, circle_radius = analyzeBinaryImageForRosa(binary_image)
    if found:
        return True, rec_time, c_h, c_w, circle_radius

    else:
        th = thr - 0.1
        return findLaserSpotRecursive(red_channel, th, max_value, start_time, rec_time)


def binarizeLaserImage(input_image, thresh, max_value):
    """
    Turn an image into a binary image.
    Inputs : input_image(3D numpy array of the red channel of the image).
             thresh(the threshold that is used as a reference to know which
                   pixels shall be turned to 0 while turning the image into
                   a binary image).
             max_value(maximum light intensity value of the input image)
    Output : binary_image(numpy array of the image turned into a binary image).
    """
    gray_image = input_image
    maximum = max_value

    half_range = 3
    retval, binary_image = threshold(
        gray_image, int(maximum * thresh)-half_range, 255, THRESH_TOZERO)
    retval, binary_image = threshold(
        binary_image, int(maximum * thresh)+half_range, 255, THRESH_BINARY)

    return binary_image


# if __name__ == "__main__":
def mainRosa(image_path):
    """
    Import an image as a numpy array and give parameters of the blob.
    Input: image_path(file path of the image you want to import. Must not
                include accents [è, é, etc.], or else it will not work).
    Output: blob(a dictionary containting parameters from the blob in the
                picure, which is the output of the formatBlob function).
    """
    
    image = cv2.imread(image_path)
    print("le type est : ", type(image))
    image_size = image.shape

    blob, rec_time, found = findLaserSpotMainCall(image)

    return blob



    # import matplotlib.pyplot as plt
#     center = (int(blob['center']['x']*image_size[1]), int(blob['center']['y']*image_size[0]))
#     radius = int(blob['radius']*image_size[0])
#     cv2.circle(image, center, radius, (255,0,0), 2)

#     image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#     plt.imshow(image_rgb)
#     plt.show()


