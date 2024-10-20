import ArducamSDK
import argparse
import time
import signal
import cv2
import ArducamSDK

from Arducam import *
from ImageConvert import *

exit_ = False


def sigint_handler(signum, frame):
    global exit_
    exit_ = True


signal.signal(signal.SIGINT, sigint_handler)
signal.signal(signal.SIGTERM, sigint_handler)


def display_fps(index):
    display_fps.frame_count += 1

    current = time.time()
    if current - display_fps.start >= 1:
        print("fps: {}".format(display_fps.frame_count))
        display_fps.frame_count = 0
        display_fps.start = current


display_fps.start = time.time()
display_fps.frame_count = 0

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-f', '--config-file', type=str, required=True, help='Specifies the configuration file.')
    parser.add_argument('-v', '--verbose', action='store_true', required=False, help='Output device information.')
    parser.add_argument('--preview-width', type=int, required=False, default=-1, help='Set the display width')
    parser.add_argument('-n', '--nopreview', action='store_true', required=False, help='Disable preview windows.')
    

    args = parser.parse_args()
    config_file = args.config_file
    verbose = args.verbose
    preview_width = args.preview_width
    no_preview = args.nopreview

    camera = ArducamCamera()

    if not camera.openCamera(config_file):
        raise RuntimeError("Failed to open camera.")
    print('camera.handle')	
    print(camera.handle)	
    REG = 0x3028, 0x0010
    if verbose:
        camera.dumpDeviceInfo()

    camera.start()
    print('ArducamSDK.Py_ArduCam_readSensorReg')
    print(ArducamSDK.Py_ArduCam_readSensorReg(camera.handle,0x3012))
    scale_width = preview_width
    ind = 1
    for i in range(4):
        ArducamSDK.Py_ArduCam_writeSensorReg(camera.handle,0x3012,ind)
        ret, data, cfg = camera.read()
        display_fps(0)
        if no_preview:
            continue

        if ret:
            image = convert_image(data, cfg, camera.color_mode)
            cv2.imwrite("Arducam%.4d.png"%(ind), image)
        else:
            print("timeout")
        ind += 10
        key = cv2.waitKey(1)
        if key == ord('q'):
            exit_ = True
        elif key == ord('s'):
            np.array(data, dtype=np.uint8).tofile("image.raw")

    camera.stop()
    camera.closeCamera()
