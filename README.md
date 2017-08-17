***Please note: This is a prototype and data is only saved to memory so it will dissapear when the application is closed.*** (The reason for saving to memory instead of saving to the disk is that we are still making large changes in the database code)

# Buddhist Well-Being

*Buddhist Well-Being* is a happiness and well-being diary application inspired by Buddhist ethics

It's a cross-platform desktop application and is in an early development/prototype stage

**Table of contents:**

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Feedback](#feedback)


## Description

A digital Buddhist diary for laypeople, at present there are four journals:
* Study
* Practice
* Engaged practice
* Gratitude and play

### Background

Having studied wellness factors (as part of an online course in positive psychology) i was not satisfied with the factors that i found so i started looking into the Buddhist tradition where i have a background, and found a text in the book "Old Path, White Clouds" (by Thich Nhat Hanh) which directed at laypeople and was very practical. This stuck with me for some time and eventually i decided to start working on this project thinking that a diary application would be a useful format for encouriging people to focus on these principles

### License

GPLv3


## Installation

There are no installation packages but it's really simple to install by following these steps:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip3 install --upgrade pip` (On Ubuntu use `sudo`)
4. On the command line: `pip3 install PyQt5` (On Ubuntu use `sudo`)
5. Download the project files from GitHub, by clicking on the "Clone or download" button and then "Download ZIP"
6. Unzip the downloaded file

### Advanced setup (optional)

Please note: *This is not necessary for running the application*, instead you can skip directly to the [usage](#usage) section

#### GNU/Linux systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - for example Gnome and KDE - you can use the bwb.desktop file included in the source (please note that if using a file manager such as the Gnome file manager you may see the name displayed as "Buddhist Well-Being" rather than the file name)

To use this file:

1. Edit the `bwb.desktop` file and change the paths to match the path that you are using
2. Copy the `bwb.desktop` file to your desktop or any place where you want to be able to start the application from
3. Copy the `bwb.desktop` file to `/usr/share/applications/` using `sudo` - this will make the application visible in any start-menu-like menu (in Lubuntu this is called the "main menu" and it's shown when clicking the button in the lower left, "vanilla" (the ordinary) Ubuntu may not have a menu like this

### Hardware recommendations

* Works best on screens with a resolution of at least 1366x768
* No network connection is needed
* Does not take much processor and memory resources, expected to run smoothly on most system 


## Usage

1. Change directory to where the software files have been extracted
2. Type and run `python3 buddhist-well-being-pyqt5.py` on GNU/Linux systems or `python buddhist-well-being-pyqt5.py` on Windows (TBD: MacOS)


## Feedback

Feedback is very welcome! If you send us feedback it can help improve the software

### Ideas for improving the software

https://www.loomio.org/g/6szAVPlR/buddhist-well-being

### Reporting bugs

Please use the GitHub issue tracker: https://github.com/SunyataZero/buddhist-well-being-pyqt5/issues

Don't hesitate to file a bug! *You are helping to improve the software*. Also if something is unclear in the *documentation* that counts as a bug as well, so please report it

### What is already working well

This is good to know so that we know what to keep, also it gives motiviation to continue working on the software
