# IMPORTANT: This project has moved to Codeberg: https://codeberg.org/fswb/well-being-diary/

# Give Up GitHub

This project has given up GitHub.  ([See Software Freedom Conservancy's *Give Up  GitHub* site for details](https://GiveUpGitHub.org).)

Any use of this project's code by GitHub Copilot, past or present, is done without our permission.  We do not consent to GitHub's use of this project's code in Copilot.

Join us; you can [give up GitHub](https://GiveUpGitHub.org) too!

# Well-being Diary

Project status: Pre-alpha

[![Join the chat at https://gitter.im/well-being-diary/Lobby](https://badges.gitter.im/well-being-diary/Lobby.svg)](https://gitter.im/well-being-diary/Lobby?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

A happiness and well-being diary application. It's a cross-platform desktop application and is in an early development/prototype stage

**Table of contents:**

1. [Description](#description)
2. [Installation](#installation)
3. [Usage](#usage)
4. [Feedback](#feedback)


## Description

The user can write questions for herself that can be used to support happiness, compassion and well-being

### Screenshots



### License

GPLv3


## Installation

There are no installation packages but it's simple to install by following these steps:

1. Download the Python 3.x installation package for your platform: https://www.python.org/downloads/
2. Install Python 3.x
3. On the command line: `pip3 install --upgrade pip` (On Ubuntu use `sudo -H`)
4. On the command line: `pip3 install PyQt5` (On Ubuntu use `sudo -H`)
5. Download the project files from GitHub, by clicking on the "Clone or download" button and then "Download ZIP"
6. Unzip the downloaded file

### Advanced setup (optional)

Please note: *This is not necessary for running the application*, instead you can skip directly to the [usage](#usage) section

#### GNU/Linux systems

For desktop systems that are compatible with the [freedesktop](https://www.freedesktop.org/) standard - for example Gnome and KDE - you can use the bwb.desktop file included in the source (please note that if using a file manager such as the Gnome file manager you may see the name displayed as "Well-being Diary" rather than the file name) to make the application visible in any start-menu-like menu (in Lubuntu this is called the "main menu" and it's shown when clicking the button in the lower left, "vanilla" (the ordinary) Ubuntu may not have a menu like this

To use this file:

1. Edit the `well-being-diary.desktop` file and change the paths to match the path that you are using
2. Copy the `well-being-diary.desktop` file to your desktop or any place where you want to be able to start the application from
3. Copy the `well-being-diary.desktop` file to `/usr/share/applications/` using `sudo`

### Hardware recommendations

* Works best on screens with a resolution of at least 1366x768
* No network connection is needed
* Does not take much processor and memory resources, expected to run smoothly on most system 


## Usage

1. Change directory to where the software files have been extracted
2. Type and run `python3 well-being-diary.py` on GNU/Linux systems or `python well-being-diary.py` on Windows

### Testing

Alternatively you can start the application with the `--testing` flag, this will make sure that the application data is stored in memory only and not saved when the application is closed

## Feedback

Feedback is very welcome! If you send us feedback it can help improve the software

### Ideas for improving the software

https://gitter.im/fswellbeing/well-being-diary

### Reporting bugs

Please use the GitHub issue tracker: https://github.com/SunyataZero/well-being-diary/issues

Don't hesitate to file a bug! *You are helping to improve the software*. Also if something is unclear in the *documentation* that counts as a bug as well, so please report it

### What is already working well

This is good to know so that we know what to keep, also it gives motiviation to continue working on the software <3
