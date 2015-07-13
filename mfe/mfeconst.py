# -*- coding: utf-8 -*-
# vim:et:sts=4:sw=4
#
# Local Variables:
# c-basic-offset: 4
# indent-tabs-mode: nil
# End:

import os
import sys

__version__  = "0.1.7"
__codename__ = "There is nothing wrong with your television set.\nDo not attempt to adjust the picture.\nWe are controlling transmission."

is_posi = os.name in ("posix", "mac")

if is_posi:
    medhome = "~/.mednafen"
    medbin  = "mednafen"
    binloc  = "/usr/games/mednafen"
    resdir  = "/usr/share/mfe"
else:
    medhome = "c:\\Program Files\\mednafen"
    medbin  = "mednafen.exe"
    binloc  = os.path.join(medhome, medbin)
    resdir  = os.path.join(medhome, "mfe")

def get_resdir():
    # when run without installing...
    exedir = os.path.dirname(os.path.realpath(sys.argv[0]))
    if os.path.exists(os.path.join(exedir, "mfe.py")):
        path = os.path.join(os.path.dirname(exedir), "resources")
        if os.path.exists(path):
            return path
    else:
        path = os.path.join(exedir, "resources")
        if os.path.exists(path):
            return path
    # when run from install
    if os.path.exists(resdir):
        return resdir
    else:
        sys.exit("Something is really broken!\n"
                 "Cant find resources directory!\n"
                 "Reinstall the program!")

resdir     = get_resdir() 
inifile    = "mfe.ini"
specfile   = os.path.join(resdir, "%s.spec" % inifile)
helpfile   = os.path.join(resdir, "mednafen.html")
#gladefile  = os.path.join(resdir, "mfe.glade")
gladefile  = os.path.join(resdir, "mfe.ui")

genimage   = os.path.join(resdir, "general.png")
engimage   = os.path.join(resdir, "engine.png")
aboutimage = os.path.join(resdir, "about.png")
clearimage = os.path.join(resdir, "clear.png")
saveimage  = os.path.join(resdir, "save.png")
docimage   = os.path.join(resdir, "doc.png")
licimage   = os.path.join(resdir, "license.png")
helpimage  = os.path.join(resdir, "help.png")
quitimage  = os.path.join(resdir, "quit.png")
playimage  = os.path.join(resdir, "play.png")
stopimage  = os.path.join(resdir, "stop.png")

#helpurl    = "http://mednafen.sourceforge.net/documentation/index.html"
helpurl    = os.path.join(resdir, "mednafen.html")

infoheader = ("<b><big>mfe %s</big></b>\n"
              "<small>\"%s\"</small>") % (__version__, __codename__)

srates = (
    "8192",
    "11025",
    "22050",
    "32000",
    "44100",
    "48000"
)

filters = (
    "none",
    "hq2x",
    "hq3x",
    "hq4x",
    "scale2x",
    "scale3x",
    "scale4x",
    "nn2x",
    "nn3x",
    "nn4x",
    "nny2x",
    "nny3x",
    "nny4x"
)

shaders = (
    "none",
    "ipxnoty",
    "ipynotx",
    "ipsharper",
    "ipxnotysharper",
    "ipynotxsharper",
    "scale2x"
)

backends = (
    "nes",
    "gb",
    "gba",
    "pce",
    "pcfx",
    "gg",
    "lynx",
    "ngp",
    "wswan",
    "sms"
)

sdrivers = (
    "oss",
    "alsa",
    "dsound",
    "sdl",
    "jack"
)

monoavail = (
    "gb",
    "gba",
    "ngp",
    "pce"
)

exts = (

    (   # NES
        ".nes"
    ),

    (   # GB(C)
        ".gb",
        ".gbc"
    ),

    (   # GBA
        ".gba"
    ),

    (   # PCE
        ".pce",
        ".tgfx",
        ".sgfx"
    ),

    (   # PCFX
    ),

    (   # GG
        ".gg"
    ),

    (   # LYNX
    ),

    (   # NGP
        ".ngp"
    ),

    (   # WS
        ".ws",
        ".wsc"
    ),

    (   # SMS
        ".sms"
    )
)

license = """The MIT License

Copyright (c) 2008 Jordan Callicoat <MonkeeSage@gmail.com>

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE."""

help = """Everything should be obvious.
If something is not, please email me at:
MonkeeSage@gmail.com

The following mappings exist:

Snapshots	→	-path_snap ...
Save Mem	→	-path_sav ...
Save States	→ 	-path_state ...
Movies		→	-path_movie ...
Cheats		→	-path_cheat ...
Palettes		→	-path_palette ...

Fullscreen		→	-fs 1
Autosave		→	-autosave 1
Cheats		→	-cheats 1
OpenGL		→	-vdriver opengl / sdl

X Scale		→	-<system>.xscale(fs) ...
Y Scale		→	-<system>.yscale(fs) ...
Width		→	-<system>.xres ...
Height		→	-<system>.xres ...
Stretch		→	-<system>.stretch 1
Interpolate	→	-<system>.videoip 1
Scanlines		→	-<system>.scanlines ...
Blur			→	-<system>.vblur 1
Accumulate	→	-<system>.vblur.accum 1
Amount		→	-<system>.vblur.accum.amount ...
Video Filter	→	-<system>.special ...
Pixel Shader	→	-<system>.pixshader ...

Sound		→	-sound 1
Force Mono	→	-<system>.forcemono 1
Volume		→	-soundvol ...
Sample Rate	→	-soundrate ...
Sound Driver	→	-sounddriver ..."""
