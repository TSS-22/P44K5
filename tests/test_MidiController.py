import pytest
import sys
import os
import json

from source.midi_controller import MidiController


@pytest.mark.parametrize(
    "pad_value, expected note",
    [
        (36,),
        (37,),
        (38,),
        (39,),
        (40,),
        (41,),
        (42,),
        (43,),
    ],
)
def test_key_degree_switch(pad_value, expected):
    midi_controller = MidiController()
    midi_controller.select_playMode(25)
    midi_controller.select_base_note(12)
    midi_controller.select_key_note(75)
    assert midi_controller.selected_pad_interval == expected
