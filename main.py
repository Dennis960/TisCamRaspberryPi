# Ararvis python videcapture
import gi
gi.require_version("Aravis", "0.8")
from gi.repository import Aravis

import cv2
import ctypes
import numpy as np

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
    im = np.ctypeslib.as_array(ptr, (buf.get_image_height(), buf.get_image_width()))
    im = im.copy()
    return im

camera=Aravis.Camera()
print("Camera found: ", camera.get_device_id())

stream=camera.create_stream(None,None)
stream.push_buffer(Aravis.Buffer.new_allocate(camera.get_payload()))
camera.start_acquisition()

while True:
    buf = stream.pop_buffer()
    print(buf) 
    if buf:
        frame = convert(buf)
        stream.push_buffer(buf) #push buffer back into stream

        cv2.imshow("frame", frame)
        ch = cv2.waitKey(1) & 0xFF
        if ch == 27 or ch == ord('q'):
            break
        elif ch == ord('s'):
            cv2.imwrite("imagename.png",frame)


camera.stop_acquisition()