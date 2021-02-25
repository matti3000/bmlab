"""
Module to perform common image operations.
"""

import numpy as np


def set_orientation(image, rotate=0, flip_ud=False, flip_lr=False):
    """
    Change the orientation of an image.

    The orientation of the raw images is setup dependent.

    Parameters
    ----------
    image: array_like
        Array of two dimensions.
    rotate: integer, default = 0
        Number of times the array is rotated by 90 degrees (clockwise).
    flip_ud: bool, default = False
        If True, flip the image up-down
    flip_lr: bool, default = False
        If True, flip the image left-right

    Returns
    -------
    image: array_like
        The input image in the requested orientation. The order
        of the operations is equal to the order
        of the input arguments: rotate, flip up-down, flip left right

    See Also
    --------
    numpy.rot90, numpy.flipud, numpy.fliplr
    """
    if not np.shape(np.shape(image)) == (2,):
        raise ValueError('Given Argument is not a two dimensional array')

    if rotate > 0:
        image = np.rot90(image, k=rotate, axes=(1, 0))

    if flip_ud:
        image = np.flipud(image)

    if flip_lr:
        image = np.fliplr(image)

    return image


def find_max_in_radius(img, xy0, radius):
    """
    Returns the index of the max. value in a circle around given point.

    Parameters
    ----------
    img: numpy.ndarray (2D)
        the image data
    xy0: tuple
        x-y indices of point around which to search for maximum
    radius: float
        the radius of the search

    Returns
    -------
    out: tuple
        x-y indices of the point of max. value
    """
    x, y = list(range(img.shape[0])), list(range(img.shape[1]))
    X, Y = np.meshgrid(x, y, indexing='ij')
    x0, y0 = xy0
    flat_img = np.nan * np.ones_like(img)
    mask = (X - x0) ** 2 + (Y - y0) ** 2 <= radius ** 2
    flat_img[mask] = img[mask]
    peak_idx = np.nanargmax(flat_img)
    peak_x, peak_y = np.unravel_index(peak_idx, img.shape, order='C')
    return peak_x, peak_y


def get_extraction_masks(images, phis, length, circle, width):
    img = images[0, ...]
    masks = []
    for phi in phis:
        masks.append(circle.rect_mask(img.shape, phi, length, width))
    return masks


def extract_values_along_arc(images, orientation, phis, circle, length, width):
    masks = get_extraction_masks(images, phis, length, circle, width)
    num_images = len(images)
    values_by_img = np.zeros((num_images, len(phis)), dtype=np.float)
    for i in range(num_images):
        img = orientation.apply(images[i])
        values_by_img[i, :] = np.array(
            [np.sum(img[mask]) for mask in masks])
    return values_by_img.mean(axis=0)
