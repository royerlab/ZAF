# ZAF | Zebrafish Automated Feeder

[![Join the chat at https://gitter.im/ZAF-Zebrafish-Automatic-Feeder/community](https://badges.gitter.im/ZAF-Zebrafish-Automatic-Feeder/community.svg)](https://gitter.im/ZAF-Zebrafish-Automatic-Feeder/community?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

In the past few decades, aquatic animals have become popular model organisms in biology, spurring a growing interest in establishing aquatic facilities. Aquatic zebrafish are widely studied and relatively easy to culture using commercial systems. However, a challenging aspect of maintaining aquatic facilities is animal feeding, which is both time- and resource-consuming. To facilitate the implementation of a zebrafish colony in any laboratory, we developed an open-source fully automatic daily feeding system. We named our system ZAF for Zebrafish Automatic Feeder. ZAF is reliable, provides a standardized amount of food to every tank, is cost-efficient and easy to build. The advanced version, ZAF+, allows for the precise control of food distribution as a function of fish density per tank. Here we provide all of the instructions to build the two automatic feeding systems, from the hardware and a friendly user interface to the open-source python code. Importantly, the design is modular and can be scaled depending on user needs. Furthermore, our results confirm that ZAF and ZAF+ do not adversely affect zebrafish culture, enabling fully automatic feeding for any aquatic facility.

![ZAF+](https://user-images.githubusercontent.com/1870994/115090362-857b5680-9ec9-11eb-9445-9378e0e6fe54.png)



This repository contains:

1. A detailed [wiki](https://github.com/royerlab/ZAF/wiki) with all instructions to build and operate a ZAF system
2. The software needed for automated fish feeding system of our fish facility.

In the following we provide instructions on how to install the ZAF software on a Raspberry Pi 3 system

## How to install and use?

```bash
# Install dependencies
sudo apt install python3-pyqt5
python3 -m pip install python-crontab==2.5.1 arbol==2020.11.6

# Get ZAF+ software
mkdir -p ~/Dev/prod/zaf_data
cd Dev/prod/
git clone https://github.com/royerlab/zaf.git
cd zaf

# Start the ZAF+ software
python3 -m python.gui.gui

# Run the ZAF software
python -m python.zaf.cli run
```

## How to cite this work?

*ZAF -- an open source fully automated feeder for aquatic facilities*
Merlin Lange, Ahmet Can Solak, Shruthi Vijaykumar, Hirofumi Kobayashi,  Bin Yang, & Loic A. Royer

