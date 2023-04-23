import ctypes
import numpy as np
import cv2

def convert(buf):
    if not buf:
        return None
    pixel_format = buf.get_image_pixel_format()
    bits_per_pixel = pixel_format >> 16 & 0xff
    if bits_per_pixel == 8:
        INTP = ctypes.POINTER(ctypes.c_uint8)
    else:
        INTP = ctypes.POINTER(ctypes.c_uint16)
    addr = buf.get_data()
    ptr = ctypes.cast(addr, INTP)
    if (buf.get_image_width() == 0 or buf.get_image_height() == 0):
        return None
    im = np.ctypeslib.as_array(ptr, (buf.get_image_height(), buf.get_image_width()))
    im = im.copy()
    im = cv2.cvtColor(im, cv2.COLOR_BAYER_RG2RGB)
    return im