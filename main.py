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
    print("Captured image: ", buf.get_image_width(), buf.get_image_height())
    if (buf.get_image_width() == 0 or buf.get_image_height() == 0):
        return None
    im = np.ctypeslib.as_array(ptr, (buf.get_image_height(), buf.get_image_width()))
    im = im.copy()
    return im

camera=Aravis.Camera()
print("Camera found: ", camera.get_device_id())
camera.set_region(0,0,640,480)
camera.set_pixel_format(Aravis.PIXEL_FORMAT_BAYER_RG_8)
camera.set_frame_rate(2)

stream=camera.create_stream(None,None)
stream.push_buffer(Aravis.Buffer.new_allocate(camera.get_payload()))
camera.start_acquisition()

while True:
    buf = stream.pop_buffer()
    if buf:
        try:
            frame = convert(buf)
        except Exception as e:
            print(e)
            stream.push_buffer(buf) #push buffer back into stream
            continue
        stream.push_buffer(buf) #push buffer back into stream

        if frame is None:
            print("Did not get a frame")
            continue
        
        frame = cv2.cvtColor(frame, cv2.COLOR_BAYER_RG2RGB)
        cv2.imshow("frame", frame)
        ch = cv2.waitKey(1) & 0xFF
        if ch == ord('q') or ch == 27: # 27 is the ESC key
            break
        if ch == ord('s'):
            cv2.imwrite("imagename.png",frame)

camera.stop_acquisition()