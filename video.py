

import os
from tkinter import Tk
#clip = VideoFileClip('output.mp4')

root =Tk()
from moviepy.editor import *

for f_name in os.listdir('../VP'):
    if f_name.endswith('.mov'):
        print(f_name)
        clip = VideoFileClip(f_name)

        clip = VideoFileClip(f_name)
        clip = clip.resize(0.5)
        clip = clip.subclip(2, 8)
        clip.preview()
