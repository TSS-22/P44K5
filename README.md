# P44K5

![License](https://img.shields.io/badge/license-BSD-blue)
![Python 3.13.3](https://img.shields.io/badge/python-3.13.3-blue?logo=python&logoColor=white)

![P44K5 main window snapshot](./ressources/readme/snapshot.png)

## Table of Contents

- [Presentation](#presentation)
- [Installation](#installation)
- [Usage](#usage)
- [Issues](#issues)
- [Acknowledgment](#acknowledgment)

## Presentation

P44k5 helps you create music and test theoretical concepts by providing a compact set of possibilities. It can be used to increase the potential of small 8 pads MIDI controller, or be used independantly. It's goal is to make it easy to play keys and chords to facilitate simple composition with limited means, and an easy way to test out different type of chords, mode, progressions to help learn these musical concepts and put them to practice to compose music.

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

## Issues

If you happen to encounter a bug or an issue, please open an issue indicating the steps to reproduce the issue as accurately as possible to help improve P44K5.

## Acknowledgment

This program uses third-party libraries and dependencies, which are subject to their own respective licenses. The inclusion of these dependencies does not imply endorsement or support of this program by the authors or copyright holders of those libraries. This program is provided "as is," and any use of third-party dependencies is at the user's own risk and discretion. For more information about the licenses of the dependencies, please refer to their individual license files or documentation.

P44K5 use the following dependencies:

- GUI: [PySide6](https://doc.qt.io/qtforpython-6/)
- MIDI: [mido](https://github.com/mido/mido), [python-rtmidi](https://github.com/SpotlightKid/python-rtmidi)
- Deployment: [nuitka](https://github.com/Nuitka/Nuitka)
