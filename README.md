acexperiments
=============

Experiments in Assetto Corsa

## Installation ##

All of the builds are versions of the NA Miata that comes with Assetto Corsa, so you will need a standard installation of Assetto Corsa. You will also need Content Manager, which most Assetto Corsa owners already have because it makes a lot of customization easier.

## Build 1 ##

The `build.py` script creates 48 vehicles, totalling about 6 GB.

(1) Unpack the `data.acd` file of the `ks_mazda_miata` into a `data` directory using Content Manager.

(2) Use something like the command below to build the various experimental vehicles. I did my file wrangling using Cygwin on Windows, which is why the path below is what it is. YMMV.

	python3 builder.py /cygdrive/c/Program\ Files\ \(x86\)/Steam/steamapps/common/assettocorsa ks_mazda_miata ace

This will produce a bunch of FWD Miatas and some RWD variants with differing levels of power and grip. 

(3) Copy or move all of the directories you just made to `cars` directory in AC.

(4) Go back to Content Manager to pack the `data` directory into a `data.acd` file.

(5) Still in Content Manager, replace the sounds with the original NA Miata (or something else if you prefer).

