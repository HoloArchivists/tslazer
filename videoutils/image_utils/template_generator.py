# Template Generator
# Resize template width to pfp size
# Change the Black to PFP Hue
# Output image
# Ready to add waveform
import os
from PIL import Image, ImageOps
from collections import defaultdict
import videoutils.audio_utils.audio_visualizer as audio_visualizer

def resize_template(template, pfp_width):
    
    resized_template = template.resize((pfp_width, pfp_width * template.height // template.width))
    return resized_template

def get_most_prominent_color(pfp_image):
    with Image.open(pfp_image) as pfp_image:
        pfp_image = pfp_image.convert('P', palette=Image.ADAPTIVE, colors=5)
        pfp_image = pfp_image.convert('RGBA')
        by_color = defaultdict(int)
        for pixel in pfp_image.getdata():
            by_color[pixel] += 1
        sorted_dict = dict(sorted(by_color.items(), key=lambda item: item[1], reverse=True))
        pixeldict = iter(sorted_dict.keys())
        most_prominent, second_most_prominent = next(pixeldict), next(pixeldict)

    return (most_prominent, second_most_prominent)

def colorize_template(template, color):
    space_template = template
    _, _, _, alpha = space_template.split()
    gray = ImageOps.grayscale(space_template)
    if color[0] == (0,0,0, 255) or color[1] == (0,0,0, 255):
        result = ImageOps.colorize(gray, color[0], color[1])
    else:
        result = ImageOps.colorize(gray, color[0], (0, 0, 0, 0))
    result.putalpha(alpha)
    return result

def add_visualizer(audio_file, template):
    visualizer = audio_visualizer.generate_waveform(audio_file, color=(255,255,255))
    w = template.size[0]
    h = template.size[1]
    im = Image.new('RGBA', (w, h), (255, 0, 0, 0))
    im.paste(template)
    im.paste(visualizer, (512,2106), mask=visualizer)
    return im

def add_pfp(template, pfp):
    w = template.size[0]
    h = template.size[1]
    im = Image.new("RGBA", (w, h))
    
    im.paste(template)
    im.paste(pfp, (0, 0))
    return im
        
def generate_template(template_file, pfp_file, audio_file, download_path):
    print("[TSLAZER] VideoEngine: Generating Cover Image")
    print(f"[TSLAZER] VideoEngine: Using {template_file} for Cover Image Generation")
    template = Image.open(template_file)
    pfp = Image.open(pfp_file)
    most_prominent = get_most_prominent_color(pfp_file)
    visualizer_template = add_visualizer(audio_file, template)
    colorized_template = colorize_template(visualizer_template, most_prominent)
    new_template = resize_template(colorized_template, pfp.width)
    generated_template = add_pfp(new_template, pfp)
    generated_template.save(os.path.join(download_path, "generated_template.png"))
    print("[TSLAZER] VideoEngine: Finished Generating Cover Image")