from tkinter import *
from midi_controller import MidiController
from midi_bridge import MidiBridge
from async_tkinter_loop import async_handler, async_mainloop
import asyncio
import threading
import queue
from functools import partial
import socket
import time

midi_controller = MidiController()

midi_bridge = MidiBridge()


root = Tk()
root.geometry("500x400")
root.title("Simple calculator")
root.iconbitmap("C:/Users/hfm/Documents/GitHub/MIDI-BRIDGE-AKAI-LPD8/gui/8258044.ico")

button_1 = Button(master=root, text="Click me").pack()

label1 = Label(master=root, text=midi_controller.base_note).pack(pady=20)

# WORKS, just need to work on the UI update problem
# async def start_bridge():
#     await asyncio.to_thread(midi_bridge.start, midi_controller)


# async_handler(asyncio.ensure_future(start_bridge()))
# async_mainloop(root)


def main_loop():
    polled_msg = midi_bridge.input.poll()
    if polled_msg:
        midi_bridge.bridge_out(midi_controller.receive_message(polled_msg))
    root.update_idletasks()
    root.update()
    time.sleep(0.016)  # ~60 FPS


while True:
    main_loop()
