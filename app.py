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
#     """
#     The app entry point. This class is responsible for initializing and tearing down
#     the application, handle menu registration etc.
#     """
#     def init_app(self):

#         try:
#             app_payload = self.import_module("app")
#             menu_callback = lambda : app_payload.io_main.main()
#             self.engine.register_command("ScanData Converter", menu_callback)
        
#         except Exception:
#             import traceback
#             traceback.print_exc()
            

    ## 이게 진짜가 될수도 
    def init_app(self):
        """
        Called as the application is being initialized
        """
        self.engine.register_command(
            "ScanData Converter",
            self.launch_app,
            {"type": "studio"}
        )
    
    def launch_app(self):
        self.logger.info(" launch_app() 진입")
        try:
            self.logger.info(" launch_app() 진입")
            app_payload = self.import_module("app")
            app_payload.io_main.main()
            

        except Exception as e:
            self.logger.error(" main() 실행 실패: %s" % e)
            self.logger.error(traceback.format_exc())
            traceback.print_exc()

#    # 파쿠리

#     ## 이게 진짜가 될수도 
#     def init_app(self):
#         """
#         Called as the application is being initialized
#         """
#         self.logger.info(" launch_app() 진입")
#         try:
#             self.logger.info(" app 파일 진입")
#             app_payload = self.import_module("app")
#             menu_callback = lambda : app_payload.dialog.show_dialog(self)
            
#             self.engine.register_command("ScanData Converter", menu_callback)
#         except Exception :
#             self.logger.error(" main() 실행 실패")
#             traceback.print_exc()
