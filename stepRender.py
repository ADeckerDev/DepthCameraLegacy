from palette import *
from PIL import Image, ImageDraw
import tkinter as tk


path = "Luke.txt"
compress = False
scale = 10000

pal = cos(x_scale=scale)#cos(x_scale=scale)



img = Image.new(mode='RGB', size=(256, 192), color='black')
draw = ImageDraw.Draw(img)

name = path.split('.')[0]

root = tk.Tk()
root.title(name)

canvas = tk.Canvas(root, width=256, height=192, bg="black")
canvas.pack()

data_dict = {}

try:
    with open(path) as file:
        first = True
        for line in file:
            if first:
                first = False
                continue

            args = line.split(',')

            data_dict[args[0]] = float(args[1])

            pos = args[0].split('&')
            x, y = float(pos[0]), float(pos[1])


except FileNotFoundError:
    raise FileNotFoundError

sorted_by_values = dict(sorted(data_dict.items(), key=lambda item: item[1]))

i=0

previous_value=0
prev_color = ""
color = pal.get_color(0)
for key, value in data_dict.items():


    pos = key.split('&')
    x, y = float(pos[0]), float(pos[1])

    if value != previous_value:
        color = pal.get_color(i)
        i += 1
        previous_color = color
        previous_value = value

    print(color)
    convert_color = rgb_to_hex(color)
    print(convert_color)

    canvas.create_rectangle(
        x, y, x + 1, y + 1,  # A single pixel is represented as a rectangle of 1x1 size
        outline=convert_color,
        fill=convert_color
    )

    draw.point(xy=(x, y), fill=convert_color)

    img.save(name + ".png")
    print("saved")

    root.mainloop()

