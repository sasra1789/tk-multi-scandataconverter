# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.


# #Shotgrid Toolkit 에서 모든 앱이 상속받는 기본 베이스 클래스 
from sgtk.platform import Application
import traceback


class SgtkStarterApp(Application):
    """
    The app entry point. This class is responsible for initializing and tearing down
    the application, handle menu registration etc.
    """
    # 다시해보자 
    def init_app(self):
        try:
            app_payload = self.import_module("app")
        # now register a *command*, which is normally a menu entry of some kind on a Shotgun
        # menu (but it depends on the engine). The engine will manage this command and 
        # whenever the user requests the command, it will call out to the callback.

        # first, set up our callback, calling out to a method inside the app module contained
        # in the python folder of the app
            menu_callback = lambda : app_payload.dialog.show_dialog(self)
        # now register the command with the engine
            self.engine.register_command("Scandata Converter2", menu_callback)
        except Exception:
            traceback.print_exc()

