# P44K5

![License](https://img.shields.io/badge/license-BSD-blue)

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [Acknowledgment](#acknowledgment)

## Installation

### Windows

You will need to be able to create a virtual MIDI output port. At the moment it is easily doable onlyvia the use of third party tools, but the new MIDI Windows API should change that soon.

At the moment we recommend using [LoopMIDI](https://www.tobias-erichsen.de/software/loopmidi.html) for this. Once installed, open the program and create a virtual MIDI port called `P44K5_virt`. LoopMIDI will need to be running before you start P44K5 everytime.

Install Python 3.X.X. [Python download](https://www.python.org/downloads/).

Launch a terminal in the folder where P44K5 is to be installed and enter the following commands.

```
git clone https://github.com/TSS-22/P44K5.git
cd P44k5
pip install -r requirement.txt
py ./P44K5.py
```
Or you can download the latest release available, and simply unzip it in the folder where the program is ot be installed and launch `P44K5.exe`. The usage of a third party software to create a virtual MIDI output is still needed at the moment.

### Linux/MacOS (beta)

On Linux and MacOS the virtual MIDI port is created by P44K5 itself, so no third party tools are needed. 

Install Python 3.X.X. [Python download](https://www.python.org/downloads/).

Launch a terminal in the folder where P44K5 is to be installed and enter the following commands.

```
git clone https://github.com/TSS-22/P44K5.git
cd P44k5
pip install -r requirement.txt
py ./P44K5.py
```

## Usage

insert doc link

## Contributing

If you happen to encounter a bug or an issue, please open an issue indicating the steps to reproduce the issue as accurately as possible to help improve P44K5.

## Acknowledgment

This program uses third-party libraries and dependencies, which are subject to their own respective licenses. The inclusion of these dependencies does not imply endorsement or support of this program by the authors or copyright holders of those libraries. This program is provided "as is," and any use of third-party dependencies is at the user's own risk and discretion. For more information about the licenses of the dependencies, please refer to their individual license files or documentation.

P44K5 use the following dependencies:

- [PySide6](https://doc.qt.io/qtforpython-6/)
- [mido](https://github.com/mido/mido)
- [python-rtmidi](https://github.com/SpotlightKid/python-rtmidi)