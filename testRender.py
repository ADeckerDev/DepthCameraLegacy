import tkinter as tk
from PIL import Image, ImageTk
from palette import *

Request_size = 5000

# Create a Tkinter window
root = tk.Tk()
root.title("palette")

# Create an image (100x400) with random colors for demonstration
width, height = Request_size, 100
image = Image.new("RGB", (width, height), "white")

start = [255, 255, 0]
end = [0, 0, 255]
third = [0, 0, 0]
fourth = [255, 255, 255]

colors = [start, end, third, fourth]

palette = noise(9999999)

# Fill the image with a gradient for demonstration
for x in range(width):
    r, g, b = palette.get_color(x)
    for y in range(height):
        image.putpixel((x, y), (r, g, b))

# Convert the image to a Tkinter-compatible format
photo = ImageTk.PhotoImage(image)

# Add the image to a label and display it in the Tkinter window
label = tk.Label(root, image=photo)
label.pack()

# Run the Tkinter event loop
root.mainloop()
