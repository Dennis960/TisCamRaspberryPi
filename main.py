import gi
gi.require_version("Aravis", "0.8")
from gi.repository import Aravis

import cv2
from convert import convert

camera=Aravis.Camera()
print("Camera found: ", camera.get_device_id())
camera.set_region(0,0,4112,2176)
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
        
        frame_720p = cv2.resize(frame, (1280, 720))
        cv2.imshow("frame 720p", frame_720p)
        ch = cv2.waitKey(1) & 0xFF
        if ch == ord('q') or ch == 27: # 27 is the ESC key
            break
        if ch == ord('s'):
            cv2.imwrite("imagename.png",frame)
            print("Image saved to imagename.png")

camera.stop_acquisition()