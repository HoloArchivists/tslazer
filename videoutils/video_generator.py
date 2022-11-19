import subprocess
from sys import platform
import videoutils.image_utils.template_generator as template_generator
# ffmpeg -loop 1 -i generated_template.png -i melspace.m4a -c:v libx264 -tune stillimage -c:a aac -b:a 90k  -shortest melspace2.mp4
def generate_template(audio_file, pfp_file, download_path, template_file="./videoutils/templates/template_1.png"):
    template_generator.generate_template(template_file=template_file, pfp_file=pfp_file, audio_file=audio_file, download_path=download_path)

def generate_video(ffmpeglocation, audio_file, output_filename, download_path, template_image='./generated_template.png'):
    print("[TSLAZER] VideoEngine: Generating Video. This may take a few minutes.")
    command = f"\"{ffmpeglocation}\" -loop 1 -i {template_image} -i \"{audio_file}\" -c:v libx264 -tune stillimage -c:a copy -shortest \"{output_filename}.mp4\" -loglevel fatal"

    if platform.startswith("linux"):
        subprocess.run(command, cwd=download_path, shell=True, check=True) #https://github.com/HoloArchivists/tslazer/issues/1
    else:
        subprocess.run(command, cwd=download_path, check=True)
    print(f"[TSLAZER] VideoEngine: {output_filename}.mp4 Successfully Generated")