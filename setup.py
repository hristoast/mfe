#!/usr/bin/env python

import os, glob
from distutils.core import setup
from mfe.mfeconst import __version__, is_posi, medhome

dfiles = (["resources/mfe.ui", "resources/mfe.ini.spec", "resources/mednafen.html",
           "resources/quit.png", "resources/help.png", "resources/engine.png",
           "resources/about.png", "resources/clear.png", "resources/general.png",
           "resources/doc.png", "resources/license.png", "resources/stop.png",
           "resources/mfe.png", "resources/save.png", "resources/play.png"])

if is_posi:
    scripts    = [os.path.join("scripts", "mfe")]
    data_files = [("/usr/share/mfe", dfiles),
                  ("/usr/share/pixmaps", ["resources/mfe.png"]),
                  ("/usr/share/applications", ["resources/mfe.desktop"])
                 ]

else:
    scripts    = [] #os.path.join("scripts", "start_mfe.pyw")]
    data_files = [(os.path.join(medhome, "mfe"), dfiles),]

setup(name             = "mfe",
      version          = __version__,
      description      = "mednafen frontend / launcher",
      long_description = "mednafen frontend / launcher",
      author           = "Jordan Callicoat",
      author_email     = "MonkeeSage@gmail.com",
      url              = "",
      download_url     = "",
      license          = "MIT",
      platforms        = ["POSIX", "OS X", "Windows"],
      keywords         = ["Emulator", "Frontend"],
      packages         = ["mfe"],
      scripts          = scripts,
      data_files       = data_files,
      )
