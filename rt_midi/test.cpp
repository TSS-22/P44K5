#include <iostream>
#include "RtMidi.h"

int main() {
    // Create a MIDI output object
    RtMidiOut midiOut;

    // Open a virtual port
    midiOut.openVirtualPort("MyVirtualOutput");

    std::cout << "Virtual MIDI output port created. Press Enter to exit." << std::endl;

    // Send a MIDI note (optional)
    std::vector<unsigned char> message = {0x90, 60, 100}; // Note On: channel 1, note 60 (C4), velocity 100
    midiOut.sendMessage(&message);

    // Wait for user input to keep the port open
    std::cin.get();

    // Clean up
    midiOut.closePort();
    return 0;
}