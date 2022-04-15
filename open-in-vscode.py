#!/usr/bin/env python2
# -*- coding: utf-8 -*-

import locale, gettext, urllib, os, subprocess
from gi.repository import Nemo, GObject
from multiprocessing import Process

EXTENSION_NAME = "nemo-open-in-vscode"
LOCALE_PATH = "/usr/share/locale/"

locale.setlocale(locale.LC_ALL, '')
gettext.bindtextdomain(EXTENSION_NAME, LOCALE_PATH)
gettext.textdomain(EXTENSION_NAME)
intl = gettext.gettext

class OpenInVSCode(GObject.GObject, Nemo.MenuProvider):

  def __init__(self):
    pass

  def get_file_items(self, window, files):
    if len(files) != 1: return
    selected = files[0]
    if selected.get_uri_scheme() not in ['file']: return

    menu_item = Nemo.MenuItem(
      name  = 'NemoPython::open-in-vscode',
      label = intl('Open in Visual Studio Code'),
      tip   = intl('Opens the selected folder or file in Visual Studio Code'),
      icon  = 'gtk-execute'
    )
    menu_item.connect('activate', self.execute, selected)
    return menu_item,

  def get_background_items(self, window, current_folder):
    menu_item = Nemo.MenuItem(
      name  = 'NemoPython::open-in-vscode',
      label = intl('Open in Visual Studio Code'),
      tip   = intl('Opens the current folder in Visual Studio Code'),
      icon  = 'gtk-execute'
    )
    menu_item.connect('activate', self.execute, current_folder)
    return menu_item,

  def launch(self, command):
    os.system(command)

  def execute(self, menu, selected):
    uri = urllib.unquote(selected.get_uri()[7:])
    try:
      code_bin = subprocess.check_output(['which', 'code'], universal_newlines=True).rstrip()
    except:
      pass
    else:
      command = ' '.join([code_bin, uri, '--no-sandbox', '--unity-launch'])
      proc = Process(target=self.launch, args=(command,))
      proc.start()
      proc.join()
