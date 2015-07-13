# vim:et:sts=4:sw=4
#
# Local Variables:
# c-basic-offset: 4
# indent-tabs-mode: nil
# End:

import os
import sys
import subprocess

from mfeconst import binloc, inifile, is_posi, medbin, medhome, specfile

try:
    from configobj import ConfigObj
    from validate import Validator
except:
    sys.exit("ConfigObj library required!\n"
             "http://www.voidspace.org.uk/python/configobj.html")

if not is_posi:
    try:
        import ctypes
    except:
        sys.exit("ctypes library required!\n"
                 "http://starship.python.net/crew/theller/ctypes/")

class Runner:

    _proc = None

    class LocateException(Exception): pass

#    def _lin_set_priority(self, priority):
#        os.system("sudo renice -%d -p %s" % (priority, self._proc.pid))

#    def _win_set_priority(self, priority):
#        """
#        Based on code from the recipe:
#        http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/496767
#        from Bryan Niederberger
#        """
#        # FIXME: move imports...make global var to check if feature avail...
#        import win32api
#        import win32process
#        import win32con
#    
#        priorityclasses = [win32process.NORMAL_PRIORITY_CLASS,
#                           win32process.ABOVE_NORMAL_PRIORITY_CLASS,
#                           win32process.HIGH_PRIORITY_CLASS,
#                           win32process.REALTIME_PRIORITY_CLASS]

#        handle = win32api.OpenProcess(win32con.PROCESS_ALL_ACCESS, True, self._proc.pid)
#        win32process.SetPriorityClass(handle, priorityclasses[priority])

    def __init__(self):
        self.mednafen = self.locate(binloc)

    def locate(self, default):
        if os.path.exists(default):
            return default
        else:
            if is_posi:
                paths = os.getenv("PATH", "").split(":")
            else:
                paths = os.getenv("PATH", "").split(";")
            for path in paths:
                path = os.path.expanduser(path)
                try:
                    for file in os.listdir(path):
                        if file == medbin:
                            return os.path.join(path, file)
                except OSError:
                    continue
        raise self.LocateException()

    def run(self, options, priority=0):
        cmd = "%s %s" % (self.mednafen, " ".join(options))
        print cmd
        self._proc = subprocess.Popen([self.mednafen] + options)
#        if priority:
#            if is_posi:
#                self._lin_set_priority(priority / 5)
#            else:
#                self._win_set_priority(priority / 25)

    def running(self):
        if self._proc and self._proc.poll() == None:
            return True
        else:
            self._proc = None
            return False

    def stop(self):
        if self._proc:
            if is_posi:
                os.kill(self._proc.pid, 9)
            else:
                ctypes.windll.kernel32.TerminateProcess(int(self._proc._handle), -1)
            self._proc = None

class Config:

    class CreateConfigPathError(Exception): pass

    def _get_config(self, path):
        validator = Validator()
        self.config = ConfigObj(path, configspec=specfile)
        self.config.validate(validator)

    def _make_dirs(self):
        for key, value in self.items():
            if key.endswith("_path"):
                path = os.path.expanduser(value)
                if not os.path.exists(path):
                    try: os.makedirs(path)
                    except: pass

    def __init__(self):
        localpath = os.path.join(os.curdir, inifile)
        if os.path.exists(localpath):
            self._get_config(localpath)
            self._make_dirs()
            return

        homepath = os.path.join(os.path.expanduser(medhome), inifile)
        if os.path.exists(homepath):
            self._get_config(homepath)
            self._make_dirs()
            return

        # write default config since none found...
        self.config = ConfigObj(configspec=specfile)
        self.config.filename = homepath
        self.config["default"] = {}
        self.config["default"]["snap_path_sar"]    = False
        self.config["default"]["save_path_sar"]    = False
        self.config["default"]["state_path_sar"]   = False
        self.config["default"]["movie_path_sar"]   = False
        self.config["default"]["cheat_path_sar"]   = False
        self.config["default"]["palette_path_sar"] = False
        self.config["default"]["snap_path"]        = os.path.join(medhome, "snaps")
        self.config["default"]["save_path"]        = os.path.join(medhome, "sav")
        self.config["default"]["state_path"]       = os.path.join(medhome, "sav")
        self.config["default"]["movie_path"]       = os.path.join(medhome, "movies")
        self.config["default"]["cheat_path"]       = os.path.join(medhome, "cheats")
        self.config["default"]["palette_path"]     = os.path.join(medhome, "palettes")
        self.config["default"]["fullscreen"]       = False
        self.config["default"]["sound"]            = True
        self.config["default"]["cheats"]           = False
        self.config["default"]["opengl"]           = True
        self.config["default"]["vsync"]            = True
        self.config["default"]["priority"]         = 0
        self.config["default"]["autosave"]         = False
        self.config["default"]["srate"]            = 3
        if is_posi:
            self.config["default"]["sdriver"]      = 1
        else:
            self.config["default"]["sdriver"]      = 2
        self.config["default"]["mono"]             = False
        self.config["default"]["volume"]           = 100
        self.config["default"]["xscale"]           = 3.0
        self.config["default"]["yscale"]           = 3.0
        self.config["default"]["xres"]             = 800
        self.config["default"]["yres"]             = 600
        self.config["default"]["stretch"]          = True
        self.config["default"]["interpolate"]      = False
        self.config["default"]["scanlines"]        = 0
        # self.config["default"]["vblur"]            = False
        self.config["default"]["accumulate"]       = False
        self.config["default"]["amount"]           = 0
        self.config["default"]["filter"]           = 0
        self.config["default"]["shader"]           = 0
        self.config["default"]["backend"]          = 0
        self.config["default"]["rom"]              = ""
        self.config["default"]["options"]          = ""
        cfgdir = os.path.dirname(homepath)
        if not os.path.isdir(cfgdir):
            try: os.makedirs(cfgdir)
            except: raise self.CreateConfigPathError(cfgdir)
        self._make_dirs()
        self.config.write()

    def __getitem__(self, key):
        return self.config["default"][key]

    def __setitem__(self, key, value):
        self.config["default"][key] = value

    def write(self):
        self.config.write()

    def items(self):
        return self.config["default"].items()

def get_med_version(medbin):
    pipe = subprocess.Popen([medbin], stdout=subprocess.PIPE)
    info = pipe.communicate()[0].strip()
    if info:
        version = info.split("\n")[0].split(" ")[2]
    else:
        version = "N/A"
    pipe.stdout.close()
    return version



