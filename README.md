# ZAF | Zebrafish Automated Feeder

In the past few decades, aquatic animals have become popular model organisms in biology, spurring a growing interest in establishing aquatic facilities. Aquatic zebrafish are widely studied and relatively easy to culture using commercial systems. However, a challenging aspect of maintaining aquatic facilities is animal feeding, which is both time- and resource-consuming. To facilitate the implementation of a zebrafish colony in any laboratory, we developed an open-source fully automatic daily feeding system. We named our system ZAF for Zebrafish Automatic Feeder. ZAF is reliable, provides a standardized amount of food to every tank, is cost-efficient and easy to build. The advanced version, ZAF+, allows for the precise control of food distribution as a function of fish density per tank. Here we provide all of the instructions to build the two automatic feeding systems, from the hardware and a friendly user interface to the open-source python code. Importantly, the design is modular and can be scaled depending on user needs. Furthermore, our results confirm that ZAF and ZAF+ do not adversely affect zebrafish culture, enabling fully automatic feeding for any aquatic facility.

![ZAF+](https://user-images.githubusercontent.com/1870994/115090362-857b5680-9ec9-11eb-9445-9378e0e6fe54.png)



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

