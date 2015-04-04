# Project Alpha

Visit our blog for news, updates, and videos:

http://townhallpinball.org

## About

Town Hall Pinball Studios is working on a customized pinball machine. The
overall plan is to:

* Use an existing pinball machine, "No Fear"
* Completely rebrand it with a new play-field, backglass, and cabinet artwork
* Design a new theme
* Design a new ruleset
* Design and/or use new animations, sound effects, and music

We are using the
[P-ROC](http://www.pinballcontrollers.com/index.php/products/p-roc)
to interface with the pinball machine and the
[Mission Pinball Framework](https://missionpinball.com/)
to implement the game.

Since the theme and the name of the game has not yet been decided,
this repository will be called "project-alpha" for now. It will be renamed
in the future.

Feel free to clone the repository and see development in action. This code
can be run without an actual pinball machine. Anything and everything can be
broken at anytime.

## Requirements

* [VirtualBox](https://www.virtualbox.org/)
* [Vagrant](https://www.vagrantup.com/)

#### Mac OS X Specific

* X11, [Xquartz](http://xquartz.macosforge.org/trac/wiki)

#### Windows Specific

* [Cygwin](https://www.cygwin.com)
* X11, [Xming](https://sourceforge.net/projects/xming/files/latest/download)

## Running

Setup a development environment as follows:

Open a terminal (open Cygwin in Windows):

```bash
mkdir town-hall-pinball
cd town-hall-pinball
```

If you are not contributing back to the repositories or prefer to use https:
```bash
git clone https://github.com/town-hall-pinball/project-alpha.git
```

Otherwise, register your SSH key and:
```bash
git clone git@github.com:town-hall-pinball/project-alpha.git
```

Then:
``` bash
cd project-alpha
vagrant up
```

Wait for the command to complete, and run the software as follows:

```bash
vagrant ssh
TODO
```
A dot-matrix display should appear.

## Contact

We can be reached at `admin@townhallpinball.org`

