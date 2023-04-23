# Ararvis python videcapture
import gi
gi.require_version("Aravis", "0.8")
from gi.repository import Aravis

import cv2
import ctypes
import numpy as np

camera=Aravis.Camera()

if 1:
    stream=camera.create_stream(None,None)
    stream.push_buffer(Aravis.Buffer.new_allocate(camera.get_payload()))
    camera.start_acquisition()
    buf=stream.pop_buffer()
    print(buf)

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
	
print("Start acquisition")
stream=camera.create_stream(None,None)
stream.push_buffer(Aravis.Buffer.new_allocate(camera.get_payload()))
camera.start_acquisition()

while True:
	buffer = stream.try_pop_buffer()
	print(buffer) 
	if buffer:
		frame = convert(buffer)
		stream.push_buffer(buffer) #push buffer back into stream

		cv2.imshow("frame", frame)
		ch = cv2.waitKey(1) & 0xFF
		if ch == 27 or ch == ord('q'):
			break
		elif ch == ord('s'):
			cv2.imwrite("imagename.png",frame)


camera.stop_acquisition()