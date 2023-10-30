from picamera2 import Picamera2, Preview
from os.path import join
import time

class RPiCamera:
    def __init__(self) -> None:
        # initialize camera
        picam2 = Picamera2()
        preview_config = picam2.create_preview_configuration(main={"size": (640, 480)})
        picam2.configure(preview_config)
        picam2.start_preview(Preview.QTGL)
        # --
        controls = {
            "ExposureTime": 20000,
            "AeEnable": 0,
            "AwbEnable": 0,
            "ColourGains":  (0.5, 1.0)
        }
        
        picam2.set_controls(controls)
        time.sleep(2)

        self.camera = picam2

    def set_exposure(self, exposure_val_ms):
        self.camera.set_controls({"ExposureTime": exposure_val_ms})

    def capture_image(self, filename, verbose=True, verbose_c=False):
        self.camera.capture_file(filename)

if __name__ == "__main__":

    # example exposure stack in milliseconds
    exposure_stack = [10000.0, 100000.0]
    output_folder = "output"
    # ----------------------------
    camera = RPiCamera()

    for exposure in exposure_stack:
        camera.set_exposure(exposure)
        camera.capture_image( join(output_folder, f"test_{exposure}"))