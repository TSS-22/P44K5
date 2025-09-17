import tkinter as tk
import time as time
from gui.ui_canvas import UiCanvas
from source.midi_controller import MidiController
from source.midi_bridge import MidiBridge


# Logic
midi_controller = MidiController()
midi_bridge = MidiBridge()

# GUI
canvas_height = 1200
canvas_width = 760

root = tk.Tk()
root.title("8P4K Power House")
root.geometry(f"{canvas_height}x{canvas_width}")
root.resizable(width=False, height=False)

main_canvas = UiCanvas(master=root)


def main_loop():
    polled_msg = midi_bridge.input.poll()
    if polled_msg:
        midi_bridge.bridge_out(midi_controller.receive_message(polled_msg))
    root.update_idletasks()
    root.update()
    time.sleep(0.016)  # ~60 FPS


while True:
    main_loop()
