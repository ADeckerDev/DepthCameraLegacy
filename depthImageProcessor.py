from PIL.Image import blend

from palette import *
from PIL import Image, ImageDraw
import tkinter as tk
################################ User interface \/ #######################



path = "TXT Files/Bass.txt"
scale = 100 # A scale around 2 recomended for the cos, and noise methods, but a scale of around 255 is generally recomended for interpolation palettes, and hsl cycle

# some example colors
red = (255, 0, 0)
orange = (255, 165, 0)
yellow = (255, 255, 0)
green = (0, 128, 0)
blue = (0, 0, 255)
indigo = (75, 0, 130)
violet = (238, 130, 238)
colors = (red, orange, yellow, green, blue, indigo, violet)

# here's where you can initialize the palette
#pal = singular_linear_interpolation(red, blue)
#pal = multiple_linear_interpolation(colors)
pal = hsl_cycle()
#pal = noise()
#pal = cos()

###################### Image Renderer ##########################
img = Image.new(mode='RGB', size=(256, 192), color='black')
draw = ImageDraw.Draw(img)

name = path.split('.')[0]

root = tk.Tk()
root.title(name)

canvas = tk.Canvas(root, width=256, height=192, bg="black")
canvas.pack()

try:
    with open(path) as file:
        first = True
        for line in file:
            if first:
                first = False
                continue

            args = line.split(',')

            pos = args[0].split('&')
            x, y = float(pos[0]), float(pos[1])

            colorRGB = pal.get_color(float(args[1])  * scale)
            color = rgb_to_hex(colorRGB)

            canvas.create_rectangle(
                x, y, x + 1, y + 1,  # A single pixel is represented as a rectangle of 1x1 size
                outline=color,
                fill=color
            )

            draw.point(xy=(x, y), fill=color)

        img.save(name + ".png")
        print("saved")

        root.mainloop()



except FileNotFoundError:
    raise FileNotFoundError