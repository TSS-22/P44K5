from tkinter import *
from PIL import Image, ImageTk
import random

# Create the main window
root = Tk()
root.title("8P4K Power House")
root.geometry("1200x880")
root.resizable(width=False, height=False)

# Load a square image (replace with your image path)
image = Image.open("background-UI.png")  # Ensure the image is square (e.g., 200x200)
image = image.resize((1200, 880))  # Resize if needed
tk_image = ImageTk.PhotoImage(image)

# Load a square image (replace with your image path)
img_wheel_mode = Image.open(
    "wheel_mode.png"
)  # Ensure the image is square (e.g., 200x200)
img_wheel_mode = img_wheel_mode.resize((170, 170))  # Resize if needed
tk_img_wheel_mode = ImageTk.PhotoImage(img_wheel_mode)

# Load a square image (replace with your image path)
img_knob_mode = Image.open(
    "knob_arrow.png"
)  # Ensure the image is square (e.g., 200x200)
img_knob_mode = img_knob_mode.resize((195, 145))  # Resize if needed
tk_img_knob_mode = ImageTk.PhotoImage(img_knob_mode)

# Load a square image (replace with your image path)
img_wheel_play = Image.open(
    "wheel_play.png"
)  # Ensure the image is square (e.g., 200x200)
img_wheel_play = img_wheel_play.resize((170, 170))  # Resize if needed
tk_img_wheel_play = ImageTk.PhotoImage(img_wheel_play)


tk_img_knob_play = ImageTk.PhotoImage(img_knob_mode)
tk_img_knob_base = ImageTk.PhotoImage(img_knob_mode)
tk_img_knob_key = ImageTk.PhotoImage(img_knob_mode)
tk_img_knob_play = ImageTk.PhotoImage(img_knob_mode)

# Create a canvas
canvas = Canvas(root, bg="#340006", width=1200, height=880)
canvas.pack()

# Position arc
# (x0, y0) ------------------
# |                         |
# |       Arc is drawn      |
# |       inside this       |
# |       rectangle         |
# |                         |
# ------------------- (x1, y1)
# x0 = center_x - radius
# y0 = center_y - radius
# x1 = center_x + radius
# y1 = center_y + radius

arc_color = "#00ff00"
# Arc base note
test_id_arc = canvas.create_arc(
    101 - 100,
    475 - 100,
    101 + 100,
    475 + 100,  # Bounding box (x0, y0, x1, y1)
    start=0,  # Start angle (degrees)
    extent=200.8125,  # Extent (degrees)
    fill="#00ff00",  # Fill color
    outline="",  # Outline color
)


# Arc base key
canvas.create_arc(
    1093 - 100,
    475 - 100,
    1093 + 100,
    475 + 100,  # Bounding box (x0, y0, x1, y1)
    start=0,  # Start angle (degrees)
    extent=200.8125,  # Extent (degrees)
    fill="#00ff00",  # Fill color
    outline="",  # Outline color
)

rct_x = 330
rct_y = 503
rct_w = 80
rct_h = rct_w
# Create a rectangle
# Parameters: x0, y0, x1, y1 (bounding box)
canvas.create_rectangle(
    rct_x - rct_w,
    rct_y - rct_w,  # Top-left corner
    rct_x + rct_w,
    rct_y + rct_w,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)

rct_space_x = 80 * 2 + 20
rct_space_y = 80 * 2 + 17

test_id_rct_out = canvas.create_rectangle(
    rct_x - rct_w,
    rct_y - rct_w + rct_space_y,  # Top-left corner
    rct_x + rct_w,
    rct_y + rct_w + rct_space_y,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)

canvas.create_rectangle(
    rct_x - rct_w + rct_space_x,
    rct_y - rct_w + rct_space_y,  # Top-left corner
    rct_x + rct_w + rct_space_x,
    rct_y + rct_w + rct_space_y,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_w + rct_space_x * 1.98,
    rct_y - rct_w + rct_space_y,  # Top-left corner
    rct_x + rct_w + rct_space_x * 1.98,
    rct_y + rct_w + rct_space_y,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_w + rct_space_x * 2.96,
    rct_y - rct_w + rct_space_y,  # Top-left corner
    rct_x + rct_w + rct_space_x * 2.96,
    rct_y + rct_w + rct_space_y,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_w + rct_space_x,
    rct_y - rct_w,  # Top-left corner
    rct_x + rct_w + rct_space_x,
    rct_y + rct_w,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_w + rct_space_x * 1.98,
    rct_y - rct_w,  # Top-left corner
    rct_x + rct_w + rct_space_x * 1.98,
    rct_y + rct_w,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_w + rct_space_x * 2.96,
    rct_y - rct_w,  # Top-left corner
    rct_x + rct_w + rct_space_x * 2.96,
    rct_y + rct_w,  # Bottom-right corner
    fill="#0BDBEE",  # Fill color
    outline="",  # Border color
)

# RECTANGLE INTERN
rct_int_w = 59
rct_int_h = rct_int_w
color_rct_int = "#340006"
color_rct_root = "#891A25"
# Create a rectangle
# Parameters: x0, y0, x1, y1 (bounding box)
test_id_rct_in = canvas.create_rectangle(
    rct_x - rct_int_w,
    rct_y - rct_int_w,  # Top-left corner
    rct_x + rct_int_w,
    rct_y + rct_int_w,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)

rct_space_int_x = 80 * 2 + 22
rct_space_y = 80 * 2 + 17

canvas.create_rectangle(
    rct_x - rct_int_w,
    rct_y - rct_int_w + rct_space_y,  # Top-left corner
    rct_x + rct_int_w,
    rct_y + rct_int_w + rct_space_y,  # Bottom-right corner
    fill=color_rct_root,  # Fill color
    outline="",  # Border color
)

canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x,
    rct_y - rct_int_w + rct_space_y,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x,
    rct_y + rct_int_w + rct_space_y,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x * 1.96,
    rct_y - rct_int_w + rct_space_y,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x * 1.96,
    rct_y + rct_int_w + rct_space_y,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x * 2.95,
    rct_y - rct_int_w + rct_space_y,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x * 2.95,
    rct_y + rct_int_w + rct_space_y,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x,
    rct_y - rct_int_w,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x,
    rct_y + rct_int_w,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x * 1.96,
    rct_y - rct_int_w,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x * 1.96,
    rct_y + rct_int_w,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)
canvas.create_rectangle(
    rct_x - rct_int_w + rct_space_int_x * 2.96,
    rct_y - rct_int_w,  # Top-left corner
    rct_x + rct_int_w + rct_space_int_x * 2.96,
    rct_y + rct_int_w,  # Bottom-right corner
    fill=color_rct_int,  # Fill color
    outline="",  # Border color
)


# Place the image on the canvas
canvas.create_image(0, 0, anchor=NW, image=tk_image)

canvas.create_image(255, 225, anchor=CENTER, image=tk_img_wheel_mode)
canvas.create_image(255, 225, anchor=CENTER, image=tk_img_knob_mode)

canvas.create_image(955, 225, anchor=CENTER, image=tk_img_wheel_play)
canvas.create_image(955, 225, anchor=CENTER, image=tk_img_knob_play)

canvas.create_image(101, 475, anchor=CENTER, image=tk_img_knob_base)
test_id_image = canvas.create_image(1093, 475, anchor=CENTER, image=tk_img_knob_key)


# Add a label (text) on top of the image
canvas.create_text(
    101,
    677,  # Center of the image
    text="C -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

# Add a label (text) on top of the image
canvas.create_text(
    1093,
    618,  # Center of the image
    text="-3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

# Add a label (text) on top of the image
canvas.create_text(
    1093,
    618,  # Center of the image
    text="-3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

# Add a label (text) on top of the image
canvas.create_text(
    1093,
    735,  # Center of the image
    text="7",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)


test_id_label = canvas.create_text(
    rct_x,
    rct_y + rct_space_y,  # Center of the image
    text="C -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x,
    rct_y + rct_space_y,  # Center of the image
    text="D -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x * 1.96,
    rct_y + rct_space_y,  # Center of the image
    text="E -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x * 2.96,
    rct_y + rct_space_y,  # Center of the image
    text="F -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

# Add a label (text) on top of the image
canvas.create_text(
    rct_x,
    rct_y,  # Center of the image
    text="G -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x,
    rct_y,  # Center of the image
    text="A -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x * 1.96,
    rct_y,  # Center of the image
    text="B -3",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)

canvas.create_text(
    rct_x + rct_space_int_x * 2.96,
    rct_y,  # Center of the image
    text="C -2",  # Your label text
    fill=arc_color,  # Text color
    font=("Arial", 36, "bold"),  # Font style
    width=180,  # Optional: constrain text width
)


def load_image_knob():
    image = Image.open("knob_arrow.png")  # Ensure the image is square (e.g., 200x200)
    image = image.resize((195, 145))  # Resize if needed
    return image


def rotate_image(angle):
    rotated_image = load_image_knob().rotate(angle)  # Rotate by 45 degrees
    tk_rotated = ImageTk.PhotoImage(rotated_image)
    canvas.itemconfig(test_id_image, image=tk_rotated)
    canvas.image = tk_rotated  # Keep a reference


rotation = 0
arc_degr = 0
color_rct_fill = ["#340006", "#0BDBEE"]


def update_layout():
    global rotation
    global arc_degr
    rotate_image(rotation + 5)
    rotation = rotation + 5

    canvas.itemconfig(test_id_arc, start=90, extent=arc_degr - 5)
    arc_degr = arc_degr - 5

    canvas.itemconfig(test_id_label, text=f"C  {random.randint(1, 9)}")
    canvas.itemconfig(test_id_rct_out, fill=color_rct_fill[random.randint(0, 1)])
    root.after(500, lambda: update_layout())


root.after(16, lambda: update_layout())
root.mainloop()
