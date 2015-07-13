# mfe
----

![mfe logo](resources/mfe.png)

A GUI frontend for [mednafen](http://mednafen.sourceforge.net/).

Originally by Jordan Callicoat,
forked for modern systems by me.

## Installation

First, install the dependencies. On Debian-like systems this should suffice:

    apt-get install python mednafen python-gtk2 python-glade2 python-configobj

Then, as a privileged user:

    make install

This will install the executable `mfe`, just launch that and game away!

## Uninstall

To uninstall `mfe`, as a privileged user:

    make uninstall

And you're done.

## FAQ

Q) I don't have any sound!

A) Use the 'sdl' audio backend.
