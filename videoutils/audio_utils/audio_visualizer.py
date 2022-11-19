# Thanks to https://stackoverflow.com/questions/33067856/how-to-generate-this-kind-of-waveform-from-audio-in-python
# Subdivide the waveform according to the scale, for example, if the waveform is 1s long and you want to display
# 10 bars then divide into 100ms chunks. Each 100ms chunks would be a certain number of samples depending on the
# sample rate. A 48kHz sample rate has 48000 samples per second do 100ms is 4800 samples.

# Enumerate each chunk of samples and compute the minimum and maximum values

# Scale and translate the min and max values to obtain the desired screen y-coords for the box you wish to draw.
# An alternative for step 2 is to compute abs(max(samples)) for each chunk and then use the positive and negative
# of that for the min and max. this makes it symmetrical.
from pydub import AudioSegment
from matplotlib import pyplot as plot
from PIL import Image, ImageDraw
import numpy as np
import os

def generate_waveform(audio_file, color):
    src = audio_file
    path = os.path.abspath(src)
    
    audio = AudioSegment.from_file(path)
    data = np.fromstring(audio._data, np.int16)
    print(f"[TSLAZER] AudioEngine: Generating Waveform for {src}")

    BARS = 23
    BAR_HEIGHT = 300
    LINE_WIDTH = 34
    SPACING = 30
    PADDING = 100

    length = len(data)
    RATIO = length/BARS

    count = 0
    maximum_item = 0
    max_array = []
    highest_line = 0

    for d in data:
        if count < RATIO:
            count += 1

            if abs(d) > maximum_item:
                maximum_item = abs(d)

        else:
            max_array.append(maximum_item)

            if maximum_item > highest_line:
                highest_line = maximum_item

            maximum_item = 0
            count = 1

    line_ratio = highest_line / BAR_HEIGHT

    im = Image.new('RGBA', (BARS * (LINE_WIDTH + SPACING), BAR_HEIGHT + PADDING), (255, 0, 0, 0))
    draw = ImageDraw.Draw(im)

    current_x = 1
    for item in max_array:
        item_height = item/line_ratio

        current_y = (BAR_HEIGHT - item_height)/2
        coords = (current_x, current_y + PADDING, current_x + LINE_WIDTH, current_y + item_height)
        draw.rounded_rectangle(coords, radius=(LINE_WIDTH - 2)/2, fill=color)
        #draw.line(coords, fill=(169, 171, 172), width=4)
        current_x = current_x + LINE_WIDTH + SPACING
    print("[TSLAZER] AudioEngine: Finished Generating Audio Waveform")
    return im
