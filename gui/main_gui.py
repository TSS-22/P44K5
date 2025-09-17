import tkinter as tk
from PIL import Image, ImageTk
from widget_base_note import WidgetBaseNote
from widget_key_note import WidgetKeyNote
from widget_panel_mode import WidgetPanelMode
from widget_panel_play_type import WidgetPanelPlayType
from widget_panel_chord import WidgetPanelChordType
from widget_pad_grid import WidgetPadGrid


canvas_height = 1200
canvas_width = 760

color_deep_brown = "#340006"
color_pad_active = "#0BDBEE"
color_pad_root = "#891A25"
color_arcs_active = "#00ff00"
color_bckgnd = "#260006"

label_font = "Arial"
label_font_size_normal = 36

root = tk.Tk()
root.title("8P4K Power House")
root.geometry(f"{canvas_height}x{canvas_width}")
root.resizable(width=False, height=False)

image = Image.open("./res_2/png/bckgnd-app.png")
image = image.resize((canvas_height, canvas_width))  # Resize if needed
tk_image = ImageTk.PhotoImage(image)

main_canvas = tk.Canvas(
    root, bg=color_deep_brown, width=canvas_height, height=canvas_width
)
main_canvas.pack()

main_canvas.create_image(0, 0, anchor=tk.NW, image=tk_image)
widget_base_note = WidgetBaseNote(master=root, canvas=main_canvas)
widget_key_note = WidgetKeyNote(master=root, canvas=main_canvas)
widget_panel_mode = WidgetPanelMode(master=root, canvas=main_canvas)
widget_panel_play_type = WidgetPanelPlayType(master=root, canvas=main_canvas)
widget_panel_chord_type = WidgetPanelChordType(master=root, canvas=main_canvas)
widget_pad_grid = WidgetPadGrid(master=root, canvas=main_canvas)

root.mainloop()
