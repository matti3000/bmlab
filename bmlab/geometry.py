import numpy as np
import skimage.transform
from shapely.geometry import Polygon, Point


class Circle(object):
    """
    Representation of a circle.

    Wraps shapely-API for reduced complexity.
    """
    def __init__(self, center, radius):
        """
        Creates a circle instance.

        Parameters
        ----------
        center: 2-tuple
            Center of the circle.

        radius: float
            Radius of the circle.

        """
        self.center = np.array(center)
        self.radius = radius

    def point(self, phi, integer=False):
        """
        Returns the xy-coordinates of a point with given polar angle phi.

        Parameters
        ----------
        phi: float
            The polar angle (counted from 0-axis to given point).

        integer: bool
            Flag indicating whether the result should be integer
            pixel value or floating point values.

        Returns
        -------
        point: 2-tuple
            The xy-coordinates of the point.

        """
        e_r = np.array([np.cos(phi), np.sin(phi)])
        pt = self.center + self.radius * e_r
        if integer:
            pt[0] = round(pt[0])
            pt[1] = round(pt[1])
            return np.array(pt, dtype=np.int)
        return pt

    def intersection(self, rect):
        """
        Calculates the intersection of the circle with a Rectangle object.

        Parameters
        ----------
        rect: Rectangle
            the rectangle

        Returns
        -------
        intersection: list of 2-tuples
            Points of intersection.
        """
        center = Point(self.center)
        inter = center.buffer(self.radius).boundary.intersection(
            rect.poly).boundary
        return [(p.x, p.y) for p in inter]

    def angle(self, point):
        """
        Returns the polar angle for a given point.

        Parameters
        ----------
        point: 2-tuple
            The point for which to calculate the polar angle.

        Returns
        -------
        angle: float
            The polar angle.
        """
        delta = np.array(point) - self.center
        if abs(delta[0]) < 1.E-9:
            if delta[1] > 0:
                return np.pi / 2.
            return 3 * np.pi / 2.
        return np.arctan(delta[1] / delta[0])

    def rect_mask(self, img_shape, phi, length, width):
        """
        Returns a mask to extract a (rotated) rectangle along the circle.

        Parameters
        ----------
        img_shape: 2-tuple of ints
            The image shape and by the same time shape of the mask.
        phi: float
            The polar angle
        length: int
            Length of the rectangle in pixels.
        width: int
            Width of the rectangle in pixels.

        Returns
        -------
        out: numpy.ndarray
            Boolean mask with True representing a point in the rectangle.
        """
        mask = np.zeros(img_shape, dtype=np.bool)
        pt = self.point(phi, integer=True)
        phi_degree = phi / np.pi * 180.
        mask[pt[0] - width // 2:pt[0] + width // 2,
             pt[1] - length // 2:pt[1] + length // 2] = True
        return skimage.transform.rotate(mask, phi_degree + 90,
                                        center=(pt[1], pt[0]))


class Rectangle(object):
    def __init__(self, shape):
        self.poly = Polygon(
            [(0, 0), (0, shape[1]), (shape[0], shape[1]), (shape[0], 0)])
