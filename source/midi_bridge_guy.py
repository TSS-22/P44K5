import sys
import os
import rtmidi
import mido
import json
from source.utilities import correct_file_path
from source.midi_controller_output import MidiControllerOutput
import asyncio
import socket


class MidiBridge:

    def __init__(self, socket_host, socket_port):
        with open(
            correct_file_path("../data/data_settings.json"), "r"
        ) as file_settings:
            data_settings = json.load(file_settings)

        self.input_port = data_settings["name_midi_in"]
        self.output_port = data_settings["name_midi_out"]

        self.init_midi_in()
        self.init_midi_out()

        self.socket_host = socket_host
        self.socket_port = socket_port

    def init_midi_in(self):
        try:
            self.input = mido.open_input(self.input_port)
            print(f"Successfully opened MIDI input: {self.input_port}")

        except Exception as e:
            print(f"Failed to open MIDI input: {e}")
            input("Press ENTER to exit...")
            sys.exit(1)

    def init_midi_out(self):
        if os.name == "posix":
            try:
                self.rtmidi_midiout = rtmidi.MidiOut()
                self.rtmidi_midiout.open_virtual_port(self.output_port)
                print(f"Successfully created MIDI output: {self.output_port}")

            except Exception as e:
                print(f"Failed to create MIDI output: {e}")
                input("Press ENTER to exit...")
                sys.exit(1)

        else:
            print(
                f"On windows, use loopMIDI to create a virtual MIDI port named : {self.output_port}.\n https://www.tobias-erichsen.de/software/loopmidi.html"
            )

        # Connect to the virtual output port
        try:
            self.output = mido.open_output(self.output_port)
            print(f"Successfully opened MIDI output: {self.output_port}")

        except Exception as e:
            print(f"Failed to open MIDI output: {e}")
            input("Press ENTER to exit...")
            sys.exit(1)

    def start(self, midi_controller):
        print(
            f"Routing MIDI from {self.input_port} to virtual port {self.output_port}..."
        )
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen()
            conn, addr = s.accept()
            with conn:
                print("Connected by", addr)
                while True:
                    data = conn.recv(1024)
                    if not data:
                        break
                    # Process data (e.g., run logic)
                    try:
                        for msg in self.input:
                            self.bridge_out(midi_controller.receive_message(msg))

                    except KeyboardInterrupt:
                        print("Stopped.")
                    finally:
                        self.stop()
                    response = str(midi_controller.base_note).encode()
                    conn.sendall(response)

    def poll(self, midi_controller):
        print("Poll started")
        if self.input.poll():
            print("messages detected")
            for msg in self.input.poll():
                self.bridge_out(midi_controller.receive_message(msg))

    def stop(self):
        self.input.close()
        self.output.close()
        print("Shutdown.")
        # input("Press ENTER to exit...")

    def bridge_out(self, midi_controller_ouput):
        if midi_controller_ouput.messages:
            for msg in midi_controller_ouput.messages:
                self.output.send(msg)
        else:
            pass  # empty message list

    def get_selected_input(self):
        return self.input

    def get_selected_ouput(self):
        return self.output
