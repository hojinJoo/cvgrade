import numpy as np
import os
import cv2


def calculate_rms(img1, img2):
    """
    Calculates RMS error between two images. Two images should have same sizes.
    """
    if (img1.shape[0] != img2.shape[0]) or \
            (img1.shape[1] != img2.shape[1]) or \
            (img1.shape[2] != img2.shape[2]):
        raise Exception("img1 and img2 should have same sizes.")

    diff = np.abs(img1 - img2)
    diff = np.abs(img1.astype(dtype=int) - img2.astype(dtype=int))
    return np.sqrt(np.mean(diff ** 2))


noise_imgs = [cv2.imread('./project1/test_images/' + img) for img in sorted(os.listdir(
    './project1/test_images')) if 'noise' in img]
clean_imgs = [cv2.imread('./project1/test_images/' + img) for img in sorted(os.listdir(
    './project1/test_images')) if 'clean' in img]
for n, c in zip(noise_imgs, clean_imgs):
    print(calculate_rms(n, c))
