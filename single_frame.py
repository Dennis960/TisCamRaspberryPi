import gi
gi.require_version("Aravis", "0.8")
from gi.repository import Aravis

from convert import convert

def get_frame_as_cv2(width = 4112, height = 2176, exposure_us = 100000):
    """
    Get a single frame from the camera as a cv2 image

    Args:
        width (int): Width of the image
        height (int): Height of the image
        exposure (float): Exposure time in microseconds
    """
    if width < 260 or width > 4112:
        raise ValueError("Width must be between 260 and 4112")
    if height < 4 or height > 2176:
        raise ValueError("Height must be between 4 and 2176")

    camera=Aravis.Camera()
    camera.set_region(0,0,width,height)
    camera.set_pixel_format(Aravis.PIXEL_FORMAT_BAYER_RG_8)
    camera.set_frame_rate(1)
    camera.set_exposure_time(exposure_us)

    stream=camera.create_stream(None,None)
    stream.push_buffer(Aravis.Buffer.new_allocate(camera.get_payload()))
    camera.start_acquisition()

    frame = None
    while frame is None:
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
    camera.stop_acquisition()
    return frame