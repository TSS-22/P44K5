from midi_controller import MidiController
from midi_bridge import MidiBridge

# from nicegui import ui
import asyncio

midi_controller = MidiController()

midi_bridge = MidiBridge()

midi_bridge.start(midi_controller)
