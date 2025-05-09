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
            self.engine.register_command("Scandata Converter", menu_callback)
        except Exception:
            traceback.print_exc()

#     def init_app(self):

#         try:
#             app_payload = self.import_module("app")
#             menu_callback = lambda : app_payload.io_main.main()
#             self.engine.register_command("ScanData Converter", menu_callback)
        
#         except Exception:
#             import traceback
#             traceback.print_exc()
            

    # ## 이게 진짜가 될수도 
    # def init_app(self):
    #     """
    #     Called as the application is being initialized
    #     """
    #     self.engine.register_command(
    #         "ScanData Converter",
    #         self.launch_app,
    #         {"type": "studio"}
    #     )
    
    # def launch_app(self):
    #     self.logger.info(" launch_app() 진입")
    #     try:
    #         self.logger.info(" launch_app() 진입")
    #         app_payload = self.import_module("app")
    #         app_payload.io_main.main()
            

    #     except Exception as e:
    #         self.logger.error(" main() 실행 실패: %s" % e)
    #         self.logger.error(traceback.format_exc())
    #         traceback.print_exc()


    # # # 파쿠리
    # def init_app(self):
    #     """
    #     Called as the application is being initialized
    #     """
    #     self.logger.info(" launch_app() 진입") #디버깅용

    #     self.engine.register_command(
    #         "ScanData Converter",
    #         self.launch_app,
    #         {"type": "studio"}
    #     )
    
    # def launch_app(self):
    #     self.logger.info(" launch_app() 진입")
    #     try:
    #         self.logger.info(" launch_app() 진입") #디버깅용
    #         app_payload = self.import_module("app")

    #         # app_payload.io_main.main()
    #         menu_callback = lambda : app_payload.dialog.show_dialog(self)
    #         # menu_callback = lambda : app_payload.io_main.main(self)
    #         self.logger.info("dialog진입 성공") # 디버깅용 
    #         self.engine.register_command("Scandata Converter", menu_callback)
    #         self.logger.info(" ScanData Converter 진입 완료. 창을 엽니다.") # 디버깅용 
        
    #     except Exception as e:
    #         self.logger.error(" main() 실행 실패: %s" % e)
    #         self.logger.error(traceback.format_exc())
    #         traceback.print_exc()

