import os, subprocess
from os.path import join

def call_bash(bash_cmd, verbose=True, verbose_c=False):
    if verbose: print(bash_cmd)

    process = subprocess.Popen(bash_cmd, stdout=subprocess.PIPE, universal_newlines=True)

    if verbose and verbose_c:
        for line in iter(process.stdout.readline, ""):
            print(line, end="\r")
            returncode = process.poll()
            if returncode is not None:
                break
        process.stdout.close()
    else:
        output, error = process.communicate()
        if(process.returncode): print("FAILED!")

def set_exposure(exposure_val, verbose=True, verbose_c=False):
    bash_cmd = [
        "gphoto2", 
        '--set-config-value', 
        f'/main/capturesettings/shutterspeed={1.0/exposure_val}'
    ]

    call_bash(bash_cmd, verbose, verbose_c)

def capture_image(filename, verbose=True, verbose_c=False):
    bash_cmd = [
        "gphoto2", 
        '--capture-image-and-download', 
        "--filename", f"{filename}.jpg"
    ]

    call_bash(bash_cmd, verbose, verbose_c)


if __name__ == "__main__":

    # example exposure stack in seconds
    exposure_stack = [1/2000, 1/100]
    output_folder = "output"
    # ----------------------------

    for exposure in exposure_stack:
        set_exposure(exposure)
        capture_image( join(output_folder, f"test_{exposure}"))