import sys
import os
import rtmidi
import mido
import json
from init_software import correct_file_path

class MidiBridge():

    def __init__(self):
        with open(correct_file_path("data_settings.json"), "r") as file_settings:
            data_settings = json.load(file_settings)

        self.input_port = data_settings["name_midi_in"]
        self.output_port = data_settings["name_midi_out"]

        self.init_midi_in()
        self.init_midi_out()


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
            print(f"On windows, use loopMIDI to create a virtual MIDI port named : {self.output_port}.\n https://www.tobias-erichsen.de/software/loopmidi.html")

        # Connect to the virtual output port
        try:
            self.output = mido.open_output(self.output_port) 
            print(f"Successfully opened MIDI output: {self.output_port}")

        except Exception as e:
            print(f"Failed to open MIDI output: {e}")
            input("Press ENTER to exit...")
            sys.exit(1)


    def start(self):
        print(f"Routing MIDI from {self.input_port} to virtual port {self.output_port}...")
        try:
            for msg in self.input:
                self.bridge_in(msg)

        except KeyboardInterrupt:
            print("Stopped.")
        finally:
            self.stop()


    def stop(self):
        self.input.close()
        self.output.close()
        print("Shutdown.")
        # input("Press ENTER to exit...")


    def bridge_out(self, list_message):
        if list_message:
            for msg in list_message:
                if msg["message"] == "note_on" or msg["message"] == "note_off":
                    self.output.send(mido.Message(msg["message"], note=msg["note"], velocity=msg["velocity"] ))

                else:
                    self.output.send(mido.Message(msg.message, msg.control, msg.value))
        else:
            pass # empty message list


    def get_input_names(self):
        return mido.get_input_names()


    def get_output_names(self):
        return mido.get_output_names()


    def print_input_names(self):
        print(self.get_input_port)


    def print_output_names(self):
        print(self.get_output_port)


    def get_selected_input(self):
        return self.input

    def get_selected_ouput(self):
        return self.output
