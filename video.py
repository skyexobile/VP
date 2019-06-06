# importing libraries
from moviepy.editor import*
#clip = VideoFileClip('output.mp4')
clip = VideoFileClip('out.mov')
clip = clip.resize(0.3)
clip = clip.subclip(2, 4)
clip.preview(fps=50)
