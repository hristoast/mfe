#!/usr/bin/python
import os

from setuptools import setup
from mfe.mfeconst import (__version__, author, author_email,
                          description, is_posi, medhome, progname, url)

dfiles = (["resources/mfe.ui", "resources/mfe.ini.spec",
           "resources/mednafen.html", "resources/quit.png",
           "resources/help.png", "resources/engine.png",
           "resources/about.png", "resources/clear.png",
           "resources/general.png", "resources/doc.png",
           "resources/license.png", "resources/stop.png",
           "resources/mfe.png", "resources/save.png", "resources/play.png"])

if is_posi:
    scripts = [os.path.join("scripts", progname)]
    data_files = [("/usr/share/" + progname, dfiles),
                  ("/usr/share/pixmaps", ["resources/mfe.png"]),
                  ("/usr/share/applications", ["resources/mfe.desktop"])]

else:
    scripts = []
    data_files = [(os.path.join(medhome, progname), dfiles), ]

setup(name=progname,
      version=__version__,
      description=description,
      long_description=description,
      author=author,
      author_email=author_email,
      url=url,
      download_url=url,
      license="MIT",
      platforms=["POSIX", "OS X", "Windows"],
      keywords=["Emulator", "Frontend"],
      packages=["mfe"],
      scripts=scripts,
      data_files=data_files,)
