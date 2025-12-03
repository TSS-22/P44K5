import sys
import os
import rtmidi
import mido
from data.data_general import hc_name_midi_out


class MidiBridge:
    def __init__(self):
        self.input = mido.ports.BaseInput()
        self.output_port = mido.ports.BaseOutput()
        output_ports = mido.get_output_names()
        self.output_port = [
            item for item in output_ports if item.startswith(hc_name_midi_out)
        ][0]
        self.init_midi_out()

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
        try:
            for msg in self.input:
                self.bridge_out(midi_controller.receive_message(msg))

        except KeyboardInterrupt:
            print("Stopped.")
        finally:
            self.stop()

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
            pass

        return midi_controller_ouput

    def get_selected_input(self):
        return self.input

    def get_selected_ouput(self):
        return self.output

    def get_midi_input(self):
        return mido.get_input_names()

    def connect_to_controller(self, controller_name):
        self.disconnect()
        if controller_name != "":
            try:
                # IMPROVE
                # Add a status connection item in the status bar
                self.input = mido.open_input(controller_name)
                print(f"Successfully opened MIDI input: {controller_name}")

            except Exception as e:
                # IMPROVE
                # Add a popup
                print(f"Failed to open MIDI input: {e}")

    def disconnect(self):
        # check if connected first
        for ports in mido.get_input_names():
            input_port_to_close = mido.ports.BaseInput(name=ports)
            input_port_to_close.close()
        self.input.close()
