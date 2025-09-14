import tkinter as tk
from PIL import Image, ImageTk
from widget_base_note import WidgetBaseNote

canvas_height = 1200
canvas_width = 760

color_deep_brown = "#340006"
color_pad_active = "#0BDBEE"
color_pad_root = "#891A25"
color_arcs_active = "#00ff00"

label_font = "Arial"
label_font__size_normal = 36

root = tk.Tk()
root.title("8P4K Power House")
root.geometry(f"{canvas_height}x{canvas_width}")

# root.resizable(width=False, height=False)
image = Image.open("./res_2/png/bckgnd-app.png")
image = image.resize((canvas_height, canvas_width))  # Resize if needed
tk_image = ImageTk.PhotoImage(image)

main_canvas = tk.Canvas(
    root, bg=color_deep_brown, width=canvas_height, height=canvas_width
)
main_canvas.pack()

main_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
widget_base_note = WidgetBaseNote(master=root, canvas=main_canvas)


# main_canvas.create_window(
#     0, 0, anchor=tk.NW, width=168, height=415, window=widget_base_note
# )
widget_base_note.pack()


root.mainloop()
