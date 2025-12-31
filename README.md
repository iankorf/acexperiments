acexperiments
=============

Experiments in Assetto Corsa

## pwr.py (2026 Winter) ##

Power to weight ratio attempted. But one really needs to make suspension
changes as the weight goes up. Probably tire width as well. This one is harder
to do than others.

```
python3 pwr.py assettocorsa ks_mazda_miata build
```


## aero.py (2023 Summer) ##

The theme here is making a time attack Miata or Miata-equivalent with FF and
MR layouts. What is the difference in layout? How does aero improve speed and
how does aero interact with layout?

### Layouts

+ FF 63% - typical FF distribution and what "the FWD book" recommends
+ FR 52% - it's easier to remove weight from the rear in a Miata
+ MR 45% - just a guess at a MR CoG

### Aero Packages

Front aero has near 0 CD and CL around 0.4. Rear aero has 0.1 CD and 0.5 CL.
Front aero weighs 20 kg per meter of chord, while rear is half that. For
testing purposes, front was set to 0.3m and rear 0.3m.

+ Naked - no splitter or wing
+ Split - splitter only
+ Wing - wing only
+ Full - splitter and wing

### Power, Grip, Weight

Power is increased by 25% over stock. It's generally easy to unlock a bit of
extra power with bolt-ons.

The tires are meant to be more like a 200TW than the defaults. The stock values
of SV tires are 1.22 and 1.21. The ST are slightly higher. I think there's even
more difference in lateral and longitudinal grip than AC uses. I therefore went
with values of 1.3 and 1.2 for the DX and DY.

It's easy to remove weight from a vehicle, so the mass was reduced 50 kg from
1080 to 1030. Since more weight is generally removed from the rear than the
front, the CoG of the FF is a little forward (52). Front aero weighs more than
rear aero.

```
mkdir build
python3 aero.py assettocorsa ks_mazda_miata
```

You will have to fix sounds and "Pack data" later in Content Manger.


## miata.py (2021 Fall) ##

All of the builds are versions of the NA Miata that comes with Assetto Corsa,
so you will need a standard installation of Assetto Corsa. You will also need
Content Manager, which most Assetto Corsa owners already have because it makes
a lot of customization easier.

The `miatas.py` script creates 48 vehicles, totalling about 6 GB.

(1) Unpack the `data.acd` file of the `ks_mazda_miata` into a `data` directory
using Content Manager.

(2) Use something like the command below to build the various experimental
vehicles. I did my file wrangling using Cygwin on Windows, which is why the
path below is what it is. YMMV.

```
python3 miatas.py /cygdrive/c/Program\ Files\ \(x86\)/Steam/steamapps/common/assettocorsa ks_mazda_miata ace
```

This will produce a bunch of FWD Miatas and some RWD variants with differing
levels of power and grip.

(3) Copy or move all of the directories you just made to `cars` directory in
AC.

(4) Go back to Content Manager to pack the `data` directory into a `data.acd`
file.

(5) Still in Content Manager, replace the sounds with the original NA Miata (or
something else if you prefer).

(6) You may want to modify the graphic offsets.

