import tkinter as tk
from PIL import Image, ImageTk
from gui.widget_base_note import WidgetBaseNote
from gui.widget_key_note import WidgetKeyNote
from gui.widget_panel_mode import WidgetPanelMode
from gui.widget_panel_play_type import WidgetPanelPlayType
from gui.widget_panel_chord import WidgetPanelChordType
from gui.widget_pad_grid import WidgetPadGrid

from source.midi_controller import MidiController
from source.midi_bridge import MidiBridge

import time

# Logic
midi_controller = MidiController()
midi_bridge = MidiBridge()

# GUI
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


def main_loop():
    polled_msg = midi_bridge.input.poll()
    if polled_msg:
        midi_bridge.bridge_out(midi_controller.receive_message(polled_msg))
    root.update_idletasks()
    root.update()
    time.sleep(0.016)  # ~60 FPS


while True:
    main_loop()
