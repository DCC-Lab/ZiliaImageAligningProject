"""Here is what I need to do:
1. Find the ONH in the picture (will most likely have a minimum brightness
and size)
2. Approximate it as an ellipse
3. Use the middle of this ellipse to determine the reference point for the
first picture, and the shift for the subsequent pictures.
4. Discard images if the ONH is not found (retina AND related rosa images).
"""

# Import image as grayscale
# Reduce image size by some factor
# Apply gamma correction to accentuate contrasts (handle IndexError!!!)
# Find Otsu's threshold
# Turn the image into a binary image according to the threshold
# Apply a canny filter
# Apply an elliptical Hough transform
# Get the best ellipse parameters for the small picture
# Convert those parameters to make them work with the big picture
# Return (or store) the ellipse parameters


from skimage.color import rgb2gray


class RetinaImage:

    def __init__(self, image):
        self.image = image
        self.grayImage = rgb2gray(image)

    def rescaleImage(self):
        pass

    def findThreshold(self):
        pass

    def binarizeImage(self):
        pass

    def applyCannyFilter(self):
        pass

    def applyHoughTransform(self):
        pass

    def getBestEllipse(self):
        pass

    def rescaleParameters(self):
        pass

    def returnBestEllipse(self):
        pass

    # Use names under??? À regarder...




    def cleanRetinaImage(image, sigma=3):
        """Apply a filter (canny filter?) to clean the image before
        turning it into a binary image. Would have to find a good default
        sigma."""


    def binarizeRetinaImage():
        """Turn a clean image into a binary image before applying a Hough
        transform."""


    def findOpticNerveHead():
        """Tell if minimum brightness and circle size have been found,
        probably returns a bool. Maybe use the ConnectedComponents class..."""


    def findClosestCircle():
        """If the ONH was found, approximate it as a circle.
        Probably returns the circle's center coordinates and radius."""


    def determineShift():
        """Use the position of the ONH circle approximation and find how
        far it is from the center of the image, which will give us the shift
        value to apply"""
