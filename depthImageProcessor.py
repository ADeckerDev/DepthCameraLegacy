from palette import *
from PIL import Image, ImageDraw
import tkinter as tk


path = "Bass.txt"
compress = False
scale = 5

pal = cos(x_scale=scale)#cos(x_scale=scale)



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

            colorRGB = pal.get_color(float(args[1]))
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