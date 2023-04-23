import gi
gi.require_version('Aravis','0.8')
from gi.repository import Aravis

cam=Aravis.Camera()
dev=cam.get_device()

if 1:
    stream=cam.create_stream(None,None)
    stream.push_buffer(Aravis.Buffer.new_allocate(cam.get_payload()))
    cam.start_acquisition()
    buf=stream.pop_buffer()
    print(buf)