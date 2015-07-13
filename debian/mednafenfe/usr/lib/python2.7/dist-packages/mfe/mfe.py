# vim:et:sts=4:sw=4
#
# Local Variables:
# c-basic-offset: 4
# indent-tabs-mode: nil
# End:

import os
import sys
import gtk
import gobject
import webbrowser
import signal
try:
    import gtkmozembed
    have_mozembed = True
except:
    have_mozembed = False
import mfeconst
import mfeutil


class MednafenFE:

    def __init__(self):

        self.config = mfeutil.Config()

        self.create_stock_items()
#        xml = glade.XML(mfeutil.gladefile)
        builder = gtk.Builder()
        builder.add_from_file(mfeconst.gladefile)
        self.get_objects(builder)

        try:
            self.runner = mfeutil.Runner()
        except mfeutil.Runner.LocateException:
            self.errordialog.set_markup("Can't find mednafen binary! Dieing.")
            self.errordialog.run()
            sys.exit(1)

        self.setup_ui()

        builder.connect_signals({
            "on_quit"                        : self.on_quit,
            "on_play"                        : self.on_play,
            "on_snapcheck_toggled"           : self.on_snapcheck_toggled,
            "on_savecheck_toggled"           : self.on_savecheck_toggled,
            "on_statecheck_toggled"          : self.on_statecheck_toggled,
            "on_moviecheck_toggled"          : self.on_moviecheck_toggled,
            "on_cheatcheck_toggled"          : self.on_cheatcheck_toggled,
            "on_palettecheck_toggled"        : self.on_palettecheck_toggled,
            "on_soundcheck_toggled"          : self.on_soundcheck_toggled,
            "on_fscheck_toggled"             : self.on_fscheck_toggled,
            "on_glcheck_toggled"             : self.on_glcheck_toggled,
            # "on_vblurcheck_toggled"          : self.on_vblurcheck_toggled,
            # "on_accumulatecheck_toggled"     : self.on_accumulatecheck_toggled,
            "on_romchooser_file_set"         : self.on_romchooser_file_set,
            "on_licensebutton_clicked"       : self.on_licensebutton_clicked,
            "on_helpbutton_clicked"          : self.on_helpbutton_clicked,
            "on_optsclearbutton_clicked"     : self.on_optsclearbutton_clicked,
            "on_optssavebutton_clicked"      : self.on_optssavebutton_clicked,
            "on_optshelpbutton_clicked"      : self.on_optshelpbutton_clicked,
            "on_optshelpbackbutton_clicked"  : self.on_optshelpbackbutton_clicked,
            "on_optshelpclosebutton_clicked" : self.on_optshelpclosebutton_clicked,
            "on_backendcombo_changed"        : self.on_backendcombo_changed
        })

        self.window.show()
        try:
            signal.signal(signal.SIGINT, self.on_quit)
        except:
            pass
        try:
            signal.signal(signal.SIGTERM, self.on_quit)
        except:
            pass
        gtk.main()

    # utility
    def create_stock_items(self):
        # FIXME: Why don't these stock items work for buttons in win32?
        #        Seem to work fine for images...hmm
        stock_items = (
            ("mfe-general", "_General", 0, 0, "English"),
            ("mfe-engine",  "_Engine",  0, 0, "English"),
            ("mfe-about",   "_Info",    0, 0, "English"),
            ("mfe-clear",   "",         0, 0, "English"),
            ("mfe-save",    "",         0, 0, "English"),
            ("mfe-doc",     "",         0, 0, "English"),
            ("mfe-license", "_License", 0, 0, "English"),
            ("mfe-help",    "_Help",    0, 0, "English"),
            ("mfe-quit",    "_Quit",    0, 0, "English"),
            ("mfe-play",    "_Play",    0, 0, "English"),
            ("mfe-stop",    "_Stop",    0, 0, "English")
        )
        stock_files = (
            ("mfe-general", mfeconst.genimage),
            ("mfe-engine",  mfeconst.engimage),
            ("mfe-about",   mfeconst.aboutimage),
            ("mfe-clear",   mfeconst.clearimage),
            ("mfe-save",    mfeconst.saveimage),
            ("mfe-doc",     mfeconst.docimage),
            ("mfe-license", mfeconst.licimage),
            ("mfe-help",    mfeconst.helpimage),
            ("mfe-quit",    mfeconst.quitimage),
            ("mfe-play",    mfeconst.playimage),
            ("mfe-stop",    mfeconst.stopimage)
        )
        gtk.stock_add(stock_items)
        factory = gtk.IconFactory()
        for item, path in stock_files:
            pixbuf = gtk.gdk.pixbuf_new_from_file(path)
            icon_set = gtk.IconSet(pixbuf)
            factory.add(item, icon_set)
        factory.add_default()

    def get_objects(self, widgets):
        self.window             = widgets.get_object("MainWindow")
        self.notebook           = widgets.get_object("Notebook")

        self.snapchooser        = widgets.get_object("snapchooser")
        self.savechooser        = widgets.get_object("savechooser")
        self.statechooser       = widgets.get_object("statechooser")
        self.moviechooser       = widgets.get_object("moviechooser")
        self.cheatchooser       = widgets.get_object("cheatchooser")
        self.palettechooser     = widgets.get_object("palettechooser")

        self.snapcheck          = widgets.get_object("snapcheck")
        self.savecheck          = widgets.get_object("savecheck")
        self.statecheck         = widgets.get_object("statecheck")
        self.moviecheck         = widgets.get_object("moviecheck")
        self.cheatcheck         = widgets.get_object("cheatcheck")
        self.palettecheck       = widgets.get_object("palettecheck")

        self.fscheck            = widgets.get_object("fscheck")
        self.soundcheck         = widgets.get_object("soundcheck")
        self.cheatscheck        = widgets.get_object("cheatscheck")
        self.glcheck            = widgets.get_object("glcheck")
        self.vsynccheck         = widgets.get_object("vsynccheck")
        self.autosavecheck      = widgets.get_object("autosavecheck")
        self.monocheck          = widgets.get_object("monocheck")
#        self.priorityspin       = widgets.get_object("priorityspin")
        self.volumescale        = widgets.get_object("volumescale")
        self.manualoptsentry    = widgets.get_object("manualoptsentry")

        self.xscalespin         = widgets.get_object("xscalespin")
        self.yscalespin         = widgets.get_object("yscalespin")
        self.xresspin           = widgets.get_object("xresspin")
        self.yresspin           = widgets.get_object("yresspin")
        self.stretchcheck       = widgets.get_object("stretchcheck")
        self.bilinearcheck      = widgets.get_object("bilinearcheck")
        self.scanlinespin       = widgets.get_object("scanlinespin")
        # self.vblurcheck         = widgets.get_object("vblurcheck")
        self.accumulatecheck    = widgets.get_object("accumulatecheck")
        self.amountlabel        = widgets.get_object("amountlabel")
        self.amountspin         = widgets.get_object("amountspin")

        self.sratecombo         = widgets.get_object("sratecombo")
        self.sdrivercombo       = widgets.get_object("sdrivercombo")
        self.filtercombo        = widgets.get_object("filtercombo")
        self.shadercombo        = widgets.get_object("shadercombo")
        self.backendcombo       = widgets.get_object("backendcombo")
        self.romchooser         = widgets.get_object("romchooser")

        self.quitbutton         = widgets.get_object("quitbutton")
        self.playbutton         = widgets.get_object("playbutton")

        self.licensedialog      = widgets.get_object("LicenseDialog")
        self.helpdialog         = widgets.get_object("HelpDialog")
        self.optshelpwindow     = widgets.get_object("OptshelpWindow")
        self.optsscrolled       = widgets.get_object("optsscrolled")

        self.optsclearbutton    = widgets.get_object("optsclearbutton")
        self.optssavebutton     = widgets.get_object("optssavebutton")
        self.optshelpbutton     = widgets.get_object("optshelpbutton")
        self.optshelpbackbutton = widgets.get_object("optshelpbackbutton")
        self.licensebutton      = widgets.get_object("licensebutton")
        self.helpbutton         = widgets.get_object("helpbutton")
        self.aboutlabel         = widgets.get_object("aboutlabel")

        widgets.get_object("licenseview").get_buffer().set_text(mfeconst.license)
        widgets.get_object("helpview").get_buffer().set_text(mfeconst.help)

#        # creating a MessageDialog from glade file throws libglade warnings...do it manually
#        self.errordialog = gtk.MessageDialog(self.window,
#                                             gtk.DIALOG_MODAL|gtk.DIALOG_DESTROY_WITH_PARENT,
#                                             gtk.MESSAGE_ERROR, gtk.BUTTONS_OK,
#                                             None)
#        self.errordialog.set_title("Error")

        self.errordialog = widgets.get_object("ErrorDialog")

        self.optshelpwindow.firstrun = True


    def setup_ui(self):

        accelgroup = gtk.AccelGroup()
        self.window.add_accel_group(accelgroup)

        accelgroup.connect_group(gtk.keysyms.g, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_g_accel)
        accelgroup.connect_group(gtk.keysyms.n, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_n_accel)
        accelgroup.connect_group(gtk.keysyms.i, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_i_accel)
        accelgroup.connect_group(gtk.keysyms.F1, 0, gtk.ACCEL_VISIBLE,
                                 self.on_f1_accel)
        accelgroup.connect_group(gtk.keysyms.F1, gtk.gdk.SHIFT_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_shift_f1_accel)
        accelgroup.connect_group(gtk.keysyms.c, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_c_accel)
        accelgroup.connect_group(gtk.keysyms.a, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_a_accel)
        accelgroup.connect_group(gtk.keysyms.e, gtk.gdk.MOD1_MASK,
                                 gtk.ACCEL_VISIBLE, self.on_e_accel)

        if have_mozembed:
           self.mozembed = gtkmozembed.MozEmbed()
           self.mozembed.load_url("file://" + mfeconst.helpfile + "#using-cli")
           self.optsscrolled.add_with_viewport(self.mozembed)
           self.mozembed.show()
           self.mozembed.connect("location", self.location_changed)

        # ensure buttons have images...
        settings = gtk.settings_get_default()
        settings.set_long_property("gtk-button-images", True, "mfe")


        text = self.aboutlabel.get_text() % (mfeconst.infoheader,
                                             mfeutil.get_med_version(self.runner.mednafen))
        self.aboutlabel.set_markup(text)

        try:
            self.snapchooser.set_current_folder(
                os.path.expanduser(self.config["snap_path"]))
        except:
            pass
        try:
            self.savechooser.set_current_folder(
                os.path.expanduser(self.config["save_path"]))
        except:
            pass
        try:
            self.statechooser.set_current_folder(
                os.path.expanduser(self.config["state_path"]))
        except:
            pass
        try:
            self.moviechooser.set_current_folder(
                os.path.expanduser(self.config["movie_path"]))
        except:
            pass
        try:
            self.cheatchooser.set_current_folder(
                os.path.expanduser(self.config["cheat_path"]))
        except:
            pass
        try:
            self.palettechooser.set_current_folder(
                os.path.expanduser(self.config["palette_path"]))
        except:
            pass

        self.snapcheck.set_active(self.config["snap_path_sar"])
        self.savecheck.set_active(self.config["save_path_sar"])
        self.statecheck.set_active(self.config["state_path_sar"])
        self.moviecheck.set_active(self.config["movie_path_sar"])
        self.cheatcheck.set_active(self.config["cheat_path_sar"])
        self.palettecheck.set_active(self.config["palette_path_sar"])

        self.on_snapcheck_toggled(self.snapcheck)
        self.on_savecheck_toggled(self.savecheck)
        self.on_statecheck_toggled(self.statecheck)
        self.on_moviecheck_toggled(self.moviecheck)
        self.on_cheatcheck_toggled(self.cheatcheck)
        self.on_palettecheck_toggled(self.palettecheck)

        self.fscheck.set_active(self.config["fullscreen"])
        self.soundcheck.set_active(self.config["sound"])
        self.cheatscheck.set_active(self.config["cheats"])
        self.glcheck.set_active(self.config["opengl"])
        self.vsynccheck.set_active(self.config["vsync"])
#        self.priorityspin.set_value(self.config["priority"])
        self.autosavecheck.set_active(self.config["autosave"])
        self.manualoptsentry.set_text(self.config["options"])

        self.monocheck.set_active(self.config["mono"])
        self.sratecombo.set_active(self.config["srate"])
        self.sdrivercombo.set_active(self.config["sdriver"])
        self.volumescale.set_value(self.config["volume"])

        self.on_soundcheck_toggled(self.soundcheck)
        self.on_glcheck_toggled(self.glcheck)

        self.on_fscheck_toggled(self.fscheck)
        self.xscalespin.set_value(self.config["xscale"])
        self.yscalespin.set_value(self.config["yscale"])
        self.xresspin.set_value(self.config["xres"])
        self.yresspin.set_value(self.config["yres"])

        self.stretchcheck.set_active(self.config["stretch"])
        self.bilinearcheck.set_active(self.config["interpolate"])
        self.scanlinespin.set_value(self.config["scanlines"])
        # self.vblurcheck.set_active(self.config["vblur"])
        # self.accumulatecheck.set_active(self.config["accumulate"])
        self.amountspin.set_value(self.config["amount"])
        self.filtercombo.set_active(self.config["filter"])
        self.shadercombo.set_active(self.config["shader"])

        # self.on_vblurcheck_toggled(self.vblurcheck)

        self.backendcombo.set_active(self.config["backend"])
        if self.config["rom"]:
            self.guess_backend()
            self.romchooser.set_filename(self.config["rom"])

        # this comes after self.guess_backend() so it is accurate
        self.set_monocheck_sensitive()

    def update_config(self):
        self.config["snap_path_sar"]    = self.snapcheck.get_active()
        self.config["save_path_sar"]    = self.savecheck.get_active()
        self.config["state_path_sar"]   = self.statecheck.get_active()
        self.config["movie_path_sar"]   = self.moviecheck.get_active()
        self.config["cheat_path_sar"]   = self.cheatcheck.get_active()
        self.config["palette_path_sar"] = self.palettecheck.get_active()

        self.config["snap_path"]        = self.snapchooser.get_current_folder()
        self.config["save_path"]        = self.savechooser.get_current_folder()
        self.config["state_path"]       = self.statechooser.get_current_folder()
        self.config["movie_path"]       = self.moviechooser.get_current_folder()
        self.config["cheat_path"]       = self.cheatchooser.get_current_folder()
        self.config["palette_path"]     = self.palettechooser.get_current_folder()

        self.config["fullscreen"]       = self.fscheck.get_active()
        self.config["sound"]            = self.soundcheck.get_active()
        self.config["cheats"]           = self.cheatscheck.get_active()
        self.config["opengl"]           = self.glcheck.get_active()
        self.config["vsync"]            = self.vsynccheck.get_active()
#        self.config["priority"]         = int(self.priorityspin.get_value())
        self.config["autosave"]         = self.autosavecheck.get_active()

        self.config["srate"]            = self.sratecombo.get_active()
        self.config["mono"]             = self.monocheck.get_active()
        self.config["sdriver"]          = self.sdrivercombo.get_active()
        self.config["volume"]           = int(self.volumescale.get_value())

        self.config["xscale"]           = self.xscalespin.get_value()
        self.config["yscale"]           = self.yscalespin.get_value()
        self.config["xres"]             = int(self.xresspin.get_value())
        self.config["yres"]             = int(self.yresspin.get_value())

        self.config["stretch"]          = self.stretchcheck.get_active()
        self.config["interpolate"]      = self.bilinearcheck.get_active()
        self.config["scanlines"]        = int(self.scanlinespin.get_value())
        # self.config["vblur"]            = self.vblurcheck.get_active()
        # self.config["accumulate"]       = self.accumulatecheck.get_active()
        self.config["amount"]           = int(self.amountspin.get_value())

        self.config["filter"]           = self.filtercombo.get_active()
        self.config["shader"]           = self.shadercombo.get_active()

        self.config["backend"]          = self.backendcombo.get_active()

        romfile = self.romchooser.get_filename()
        if romfile:
            self.config["rom"] = romfile
        else:
            self.config["rom"] = ""

    def format_options(self):
        options = []
        rompath = os.path.dirname(self.config["rom"])
        prefix  = mfeconst.backends[self.config["backend"]]

        options.append("-path_snap")
        if self.config["snap_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["snap_path"])

        options.append("-path_sav")
        if self.config["save_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["save_path"])

        options.append("-path_state")
        if self.config["state_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["state_path"])

        options.append("-path_movie")
        if self.config["movie_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["movie_path"])

        options.append("-path_cheat")
        if self.config["cheat_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["cheat_path"])

        options.append("-path_palette")
        if self.config["palette_path_sar"]:
            options.append(rompath)
        else:
            options.append(self.config["palette_path"])

        options.append("-vdriver")
        if self.config["opengl"]:
            options.append("opengl")
            options.append("-glvsync")
            options.append(str(int(self.config["vsync"])))
            options.append("-%s.pixshader" % prefix)
            options.append(mfeconst.shaders[self.config["shader"]])
        else:
            options.append("sdl")

        options.append("-fs")
        options.append(str(int(self.config["fullscreen"])))

        options.append("-sound")
        options.append(str(int(self.config["sound"])))
        if self.config["sound"]:
            options.append("-soundrate")
            options.append(mfeconst.srates[self.config["srate"]])
            options.append("-sounddriver")
            options.append(mfeconst.sdrivers[self.config["sdriver"]])
            options.append("-soundvol")
            options.append(str(self.config["volume"]))
            if prefix in mfeconst.monoavail:
                options.append("-%s.forcemono" % prefix)
                options.append(str(int(self.config["mono"])))

        options.append("-cheats")
        options.append(str(int(self.config["cheats"])))

        options.append("-autosave")
        options.append(str(int(self.config["autosave"])))

        if self.config["fullscreen"]:
            if self.config["xscale"] > 0:
                options.append("-%s.xscalefs" % prefix)
                options.append(str(self.config["xscale"]))
            if self.config["yscale"] > 0:
                options.append("-%s.yscalefs" % prefix)
                options.append(str(self.config["yscale"]))
            if self.config["xres"] > 0:
                options.append("-%s.xres" % prefix)
                options.append(str(self.config["xres"]))
            if self.config["yres"] > 0:
                options.append("-%s.yres" % prefix)
                options.append(str(self.config["yres"]))
        else:
            if self.config["xscale"] > 0:
                options.append("-%s.xscale" % prefix)
                options.append(str(self.config["xscale"]))
            if self.config["yscale"] > 0:
                options.append("-%s.yscale" % prefix)
                options.append(str(self.config["yscale"]))
        options.append("-%s.stretch" % prefix)
        options.append(str(int(self.config["stretch"])))
        options.append("-%s.videoip" % prefix)
        options.append(str(int(self.config["interpolate"])))

        # options.append("-%s.vblur" % prefix)
        # options.append(str(int(self.config["vblur"])))
        # if self.config["vblur"]:
        #     options.append("-%s.vblur.accum" % prefix)
        #     options.append(str(int(self.config["accumulate"])))
        #     if self.config["accumulate"]:
        #         options.append("-%s.vblur.accum.amount" % prefix)
        #         options.append(str(self.config["amount"]))

        options.append("-%s.scanlines" % prefix)
        options.append(str(self.config["scanlines"]))

        options.append("-%s.special" % prefix)
        options.append(mfeconst.filters[self.config["filter"]])

        text = self.manualoptsentry.get_text().strip()
        if text:
            for item in text.split(" "):
                options.append(item)

        options.append(self.config["rom"])

        return options

    def set_monocheck_sensitive(self):
        backend = mfeconst.backends[self.backendcombo.get_active()]
        enable  = (backend in mfeconst.monoavail) & self.soundcheck.get_active()
        self.monocheck.set_sensitive(enable)

    def guess_backend(self):
        ext = os.path.splitext(self.config["rom"])[1]
        for i in range(len(mfeconst.exts)):
            if ext.lower() in mfeconst.exts[i]:
                self.backendcombo.set_active(i)

    def enable_disable_widgets(self, enable):
        if enable:
            self.playbutton.set_label("mfe-play")
        else:
            self.playbutton.set_label("mfe-stop")
        
        # FIXME: keep self.optshelpbutton always enabled?
        self.notebook.set_sensitive(enable)
        
        # no reason to stop emulation first in order to quit, right?
        #self.quitbutton.set_sensitive(enable)

    def check_alive(self):
        if self.runner.running():
            return True
        else:
            self.enable_disable_widgets(True)
            return False

    def do_play(self):
        if not self.config["rom"]:
            self.errordialog.set_markup("You must select a ROM file first!")
            self.errordialog.run()
            self.errordialog.hide()
            return
        self.update_config()
        self.runner.run(self.format_options()) #, self.config["priority"])
        gobject.timeout_add(500, self.check_alive)
        self.enable_disable_widgets(False)

    def do_stop(self):
        self.runner.stop()
        self.enable_disable_widgets(True)

    # callbacks
    def on_snapcheck_toggled(self, widget, *args):
        self.snapchooser.set_sensitive(not widget.get_active())

    def on_savecheck_toggled(self, widget, *args):
        self.savechooser.set_sensitive(not widget.get_active())

    def on_statecheck_toggled(self, widget, *args):
        self.statechooser.set_sensitive(not widget.get_active())

    def on_moviecheck_toggled(self, widget, *args):
        self.moviechooser.set_sensitive(not widget.get_active())

    def on_cheatcheck_toggled(self, widget, *args):
        self.cheatchooser.set_sensitive(not widget.get_active())

    def on_palettecheck_toggled(self, widget, *args):
        self.palettechooser.set_sensitive(not widget.get_active())

    def on_soundcheck_toggled(self, widget, *args):
        enable = widget.get_active()
        self.sratecombo.set_sensitive(enable)
        self.sdrivercombo.set_sensitive(enable)
        self.volumescale.set_sensitive(enable)
        self.set_monocheck_sensitive()

    def on_glcheck_toggled(self, widget, *args):
        enable = widget.get_active()
        self.shadercombo.set_sensitive(enable)
        self.vsynccheck.set_sensitive(enable)

    def on_fscheck_toggled(self, widget, *args):
        enable = widget.get_active()
        self.xresspin.set_sensitive(enable)
        self.yresspin.set_sensitive(enable)

    # def on_vblurcheck_toggled(self, widget, *args):
    #     enable = widget.get_active()
    #     self.accumulatecheck.set_sensitive(enable)
    #     if gtk.pygtk_version >= (2, 12, 0):
    #         # gtk.Widget.set_has_tooltip() is supposed to be there since 2.12...
    #         # well...it's not on my 2.12.1 box...whatever, do it manually...
    #         try: self.accumulatecheck.props.has_tooltip = enable
    #         except: pass
    #     self.on_accumulatecheck_toggled(self.accumulatecheck)

    # def on_accumulatecheck_toggled(self, widget, *args):
    #     enable = (widget.get_active() & self.vblurcheck.get_active())
    #     self.amountlabel.set_sensitive(enable)
    #     self.amountspin.set_sensitive(enable)
    #     if gtk.pygtk_version >= (2, 12, 0):
    #         try: self.amountspin.props.has_tooltip = enable
    #         except: pass

    def on_romchooser_file_set(self, widget, *args):
        self.config["rom"] = widget.get_filename()
        if self.config["rom"]:
            self.guess_backend()

    def on_play(self, widget, *args):
        if self.playbutton.get_label() == "mfe-play":
            self.do_play()
        else:
            self.do_stop()

    def on_licensebutton_clicked(self, widget, *args):
        self.licensedialog.run()
        self.licensedialog.hide()

    def on_helpbutton_clicked(self, widget, *args):
        self.helpdialog.run()
        self.helpdialog.hide()

    def on_optsclearbutton_clicked(self, widget, *args):
        self.config["options"] = ""
        self.manualoptsentry.set_text("")

    def on_optssavebutton_clicked(self, widget, *args):
        self.config["options"] = self.manualoptsentry.get_text()

    def on_optshelpbutton_clicked(self, widget, *args):
        if have_mozembed:
            self.optshelpwindow.show()
        else:
            webbrowser.open(mfeconst.helpurl)

    def on_optshelpclosebutton_clicked(self, widget, *args):
        self.optshelpwindow.hide()

    def on_optshelpbackbutton_clicked(self, widget, *args):
        if self.mozembed.can_go_back():
            self.mozembed.go_back()

    def location_changed(self, *args):
        if (self.mozembed.can_go_back() and
            self.mozembed.get_location().rfind("#") == -1):
            self.optshelpbackbutton.set_sensitive(True)
        else:
            self.optshelpbackbutton.set_sensitive(False)

    def on_backendcombo_changed(self, widget, *args):
        self.set_monocheck_sensitive()

    # accel callbacks
    def on_g_accel(self, group, window, keyval, modifiers):
        self.notebook.set_current_page(0)

    def on_n_accel(self, group, window, keyval, modifiers):
        self.notebook.set_current_page(1)

    def on_i_accel(self, group, window, keyval, modifiers):
        self.notebook.set_current_page(2)

    def on_f1_accel(self, group, window, keyval, modifiers):
        index = self.notebook.get_current_page()
        if index == self.notebook.get_n_pages()-1:
            self.notebook.set_current_page(0)
        else:
            self.notebook.next_page()

    def on_shift_f1_accel(self, group, window, keyval, modifiers):
        index = self.notebook.get_current_page()
        if index == 0:
            self.notebook.set_current_page(self.notebook.get_n_pages()-1)
        else:
            self.notebook.prev_page()

    def on_c_accel(self, group, window, keyval, modifiers):
        self.optsclearbutton.activate()

    def on_a_accel(self, group, window, keyval, modifiers):
        self.optssavebutton.activate()

    def on_e_accel(self, group, window, keyval, modifiers):
        self.optshelpbutton.activate()

    def on_quit(self, *args):
        # let the emulator keep running after we close, right?
        #self.runner.stop()
        self.update_config()
        self.config.write()
        gtk.main_quit()

if __name__ == "__main__":
    mfe = MednafenFE()

