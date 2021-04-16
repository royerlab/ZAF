# ZAF

Zebrafish Automated Feeder

This repository contains:

1. A detailed [wiki](https://github.com/royerlab/ZAF/wiki) with all instructions to build and operate a ZAF system
2. The software needed for automated fish feeding system of our fish facility.

In the following we provide instructions on how to install the ZAF software on a Raspberry Pi 3 system

## How to install?

```bash
git clone https://github.com/royerlab/fishfeed.git
cd fishfeed
pip install -e .

# Check installation
fishfeed -h
```

## How to use?

```bash
# To check details of last 5 run
fishfeed last5

# To check details of last 50 run
fishfeed last50

# To run feeding
fishfeed run
```

## GUI for ZAF

### Dependency
PyQt5


Use Front Panel to control across all programs.

**Add program** to add more programs

Active programs window shows the programs and day&time that set to run.

Save & load programs saves and loads programs in csv format.

Dialob box displays current status of ZAF2. 

![Alt text](python/gui/screenshots/ScreenShot1.png?raw=true "ScreenShot")

On/Off button to switch on and off the program.

Select whether to feed fish or wash tanks.

Select day and time to run the program.

Check tank number and quantity that will be fed to each tank.

A summary will show on Summary box.

![Alt text](python/gui/screenshots/ScreenShot2.png?raw=true "ScreenShot")


## How to cite this work?

*ZAF -- an open source fully automated feeder for aquatic facilities*
Merlin Lange, AhmetCan Solak, Shruthi Vijaykumar, Hirofumi Kobayashi,  Bin Yang, & Loic A. Royer

