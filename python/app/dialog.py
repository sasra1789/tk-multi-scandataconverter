# Copyright (c) 2013 Shotgun Software Inc.
#
# CONFIDENTIAL AND PROPRIETARY
#
# This work is provided "AS IS" and subject to the Shotgun Pipeline Toolkit
# Source Code License included in this distribution package. See LICENSE.
# By accessing, using, copying or modifying this work you indicate your
# agreement to the Shotgun Pipeline Toolkit Source Code License. All rights
# not expressly granted therein are reserved by Shotgun Software Inc.
import os


from .scanfile_handler import find_plate_files
from .converter import generate_mov_thumbnail, convert_exr_to_jpg_with_ffmpeg,  convert_to_mp4, convert_to_webm, generate_montage_multi, find_thumbnail_from_montage,  list_excel_versions
from .excel_manager import save_to_excel_with_thumbnails, load_excel_data,  get_next_versioned_filename
from .scan_structure import create_plate_structure
from .shotgrid_api import connect_to_shotgrid, find_shot, create_version, create_shot, list_projects
import shutil
# from PySide6.QtWidgets import QInputDialog, QFileDialog, QMessageBox
# from PySide6.QtWidgets import  QWidget

import sgtk
import os
import sys
import threading

## 테스트 
# from sgtk.platform.qt import QWidgets, QInputDialog, QFileDialog, QMessageBox
from sgtk.platform.qt import QtCore, QtGui
from .ui.dialog import Ui_Dialog
# from .main_window import MainWindow


# standard toolkit logger
logger = sgtk.platform.get_logger(__name__)


def show_dialog(app_instance):
    """
    Shows the main dialog window.
    """
    # # in order to handle UIs seamlessly, each toolkit engine has methods for launching
    # # different types of windows. By using these methods, your windows will be correctly
    # # decorated and handled in a consistent fashion by the system.

    # # we pass the dialog class to this method and leave the actual construction
    # # to be carried out by toolkit.
    # app_instance.engine.show_dialog("SScandata converter", app_instance, AppDialog)
    app_instance.engine.show_dialog("Start scandata converter", app_instance, AppDialog)

    # 여러 번 열리지 않도록
    # app.engine.show_dialog("Launching ScanData Converter...")
    # dialog = app.engine.show_dialog("ScanData Converter", app, AppDialog)
   
    # dialog = app.engine.show_dialog("ScanData Converter", app, AppDialog)
    # AppDialog(dialog)  # UI에 컨트롤러 연결

class AppDialog(QtGui.QWidget):
    """
    Main application dialog window
    """
    def __init__(self, parent=None):
        QtGui.QWidget.__init__(self)


        # now load in the UI that was created in the UI designer
        self.main_window = Ui_Dialog()
        self.main_window.setupUi(self)
        # most of the useful accessors are available through the Application class instance
        # it is often handy to keep a reference to this. You can get it via the following method:
        self._app = sgtk.platform.current_bundle()

        # logging happens via a standard toolkit logger
        logger.info("Launching Scandata Converter Application...")

        # via the self._app handle we can for example access:
        # - The engine, via self._app.engine
        # - A Shotgun API instance, via self._app.shotgun
        # - An Sgtk API instance, via self._app.sgtk

        # lastly, set up our very basic UI
        self.ui.context.setText("Current Context: %s" % self._app.context)

        super(AppDialog, self).__init__(parent)

        # self.main_window =Ui_Dialog()

        self.folder_path = ""  # 선택된 경로 저장
        self.thumb_cache_dir = "/home/rapa/show"  # 썸네일 저장 위치 위치는 나중에 바꿔주기
    
        self.setup_connections()

    def show_main_window(self):
        self.load_shotgrid_projects()
        self.main_window.show()


    #버튼 연결
    def setup_connections(self):
        self.main_window.select_button.clicked.connect(self.on_select_folder)
        self.main_window.load_button.clicked.connect(self.on_load_files)
        self.main_window.save_button.clicked.connect(self.on_save_excel)
        self.main_window.register_excel_button.clicked.connect(self.on_register_to_shotgrid)
        self.main_window.project_combo.currentTextChanged.connect(self.update_project_label)

        #모든 선택/해제버튼 하나의 토글 버튼만 연결
        self.select_all_checked = False
        self.main_window.toggle_select_button.clicked.connect(self.toggle_select_all)

    
    def on_select_folder(self):
        folder = QtGui.QFileDialog.getExistingDirectory(self.main_window, "날짜 폴더 선택")
        if not folder:
            print("X 경로 선택 안됨")
            return

        self.folder_path = folder
        self.main_window.set_path(folder)

        # 하위 폴더 자동 수집
        self.selected_folders = [
            os.path.join(folder, sub)
            for sub in os.listdir(folder)
            if os.path.isdir(os.path.join(folder, sub))
        ]


    # scanfile_handler 로 .exr, .mov 파일 읽고, 썸네일 생성 
    def on_load_files(self):
        # 기존 데이터는 유지하고 새롭게 아래에 추가하기 
        
        if not self.folder_path:
            print(" 폴더가 선택되지 않았습니다.")
            return
        
        base_row = self.main_window.table.rowCount()

        #  현재 테이블에 이미 올라간 roll 값들 추출
        existing_rolls = set()
        for row in range(base_row):
            roll_item = self.main_window.table.item(row, 2)
            if roll_item:
                existing_rolls.add(roll_item.text())
        file_items = find_plate_files(self.folder_path)

        for folder in self.selected_folders:
            file_items = find_plate_files(folder)

            for i, item in enumerate(file_items):
                if item["basename"] in existing_rolls:
                    continue  #  중복 방지

                # test3 mov 썸네일 생성
                if item["type"] == "mov":
                    thumb_path = generate_mov_thumbnail(item["first_frame_path"], self.thumb_cache_dir)
                else:
                    thumb_path = item["first_frame_path"]  # exr/jpg는 첫 프레임 사용

                table_row_data = {
                    "thumbnail": thumb_path or "",
                    "roll": item["basename"],
                    "shot_name": "S샷명_SH자동생성예정",  # 나중에 자동 태깅 가능
                    "version": "v001",                # 기본 버전
                    "type": item["type"],
                    "path": item["seq_dir"],
                }
                pass

                # test 2
                if item["type"] == "sequence":
                    thumb_jpg = os.path.join(
                        self.thumb_cache_dir,
                        os.path.splitext(os.path.basename(item["first_frame_path"]))[0] + "_thumb.jpg"
                    )
                    if not os.path.exists(thumb_jpg):
                        convert_exr_to_jpg_with_ffmpeg(item["first_frame_path"], thumb_jpg)
                    thumb_path = thumb_jpg
                else:
                    thumb_path = generate_mov_thumbnail(item["first_frame_path"], self.thumb_cache_dir)

                table_row_data = {
                    "thumbnail": thumb_path or "",
                    "roll": item["basename"],
                    "shot_name": "S샷명을_SH입력해주세요",
                    "version": "v001",
                    "type": item["type"],
                    "path": item["seq_dir"],
                }
                self.main_window.add_table_row(table_row_data, base_row + i)
                existing_rolls.add(item["basename"])


    # 파일선택 UI
    def on_select_excel_version(self):
        excel_dir = "/home/rapa/show/serin_converter"
        excel_files = list_excel_versions(excel_dir)

        if not excel_files:
            print("X 저장된 엑셀 파일이 없습니다.")
            return None

        #  사용자에게 파일 선택 받기
        file_name, ok = QtGui.QInputDialog.getItem(
            self.main_window,
            "엑셀 버전 선택",
            "샷그리드에 업로드할 엑셀 파일을 선택하세요:",
            excel_files,
            editable=False
        )

        if ok and file_name:
            selected_path = os.path.join(excel_dir, file_name)
            print(f" 선택된파일: {selected_path}")
            return selected_path
        else:
            print("⚠️ 선택 취소됨")
            return None


    # 엑셀 저장 함수 (버전 자동 증가)
    def on_save_excel(self):

        if self.main_window.table.rowCount() == 0:
            print("⚠️ 테이블에 데이터가 없습니다.")
            return

        

        # 테이블 데이터를 리스트로 추출
        data_list = []
        for row in range(self.main_window.table.rowCount()):
            checkbox = self.main_window.table.cellWidget(row, 0)
            
            if not checkbox.isChecked():
                continue  # 체크박스 체크 안하면 넘어감

            thumb_widget = self.main_window.table.cellWidget(row, 1)
            thumbnail = thumb_widget.toolTip() if thumb_widget else ""

            def safe_text(col): # 핼퍼함수 
                item = self.main_window.table.item(row, col)
                return item.text() if item else ""

            data_list.append({
                "thumbnail": thumbnail,
                "roll": safe_text(2),
                "shot_name": safe_text(3),
                "version": safe_text(4),
                "type": safe_text(5),
                "path": safe_text(6),
            })
            

        
        # 모두 체크 안될 경우 
        if not data_list:
            print("⚠️ 체크된 항목이 없습니다. 엑셀 저장을 취소합니다.")
    
            QtGui.QMessageBox.warning(self.main_window, "경고", "✔ 체크된 항목이 없습니다.")
            return


        # 에라모르겠다

        # project_name 먼저 가져오기
        project = self.get_selected_project()
        if not project:
            print("⚠️ 프로젝트가 선택되지 않았습니다.")
            QtGui.QMessageBox.warning(self.main_window, "오류", "프로젝트가 선택되지 않았습니다.")
            return
        project_name = project["name"]

        # 폴더 선택 다이얼로그 열기
        scan_root = f"/home/rapa/show/{project_name}/product/scan"
        selected_folder = QtGui.QFileDialog.getExistingDirectory(
            self.main_window,
            "날짜 폴더 선택",
            scan_root
        )
    
        if not selected_folder:
            print("⚠️ 폴더 선택이 취소되었습니다.")
            return
        
        print(f"선택된 폴더: {selected_folder}")

        # 선택된 폴더 경로 분석
        parts = selected_folder.split("/")
        try:
            scan_date_folder = parts[-2]  # 날짜폴더명
            shot_folder_name = parts[-1]  # 샷폴더명
        except IndexError:
            QtGui.QMessageBox.warning(self.main_window, "오류", "선택한 폴더 구조가 올바르지 않습니다.")
            return

        print(f" 선택한 날짜: {scan_date_folder}, 샷 폴더명: {shot_folder_name}")

        # 저장 경로: 자동 버전 증가된 .xlsx 파일 생성
        # 기존 build_excel_save_path 호출 대신:
        save_base = os.path.join(selected_folder, "scanlist.xlsx")
        save_path = get_next_versioned_filename(save_base)
        #  엑셀로 저장 (썸네일 포함)
        save_to_excel_with_thumbnails(data_list, save_path)
        print(f" 엑셀 저장 완료: {save_path}")

    def on_collect(self):
        if not self.folder_path:
            print(" 경로가 지정되지 않았습니다.")
            return

        for row in range(self.main_window.table.rowCount()):
            shot = self.main_window.table.item(row, 3).text()           # shot_name
            plate_type = self.main_window.table.item(row, 5).text()     # type
            version = self.main_window.table.item(row, 4).text()        # version
            src_path = self.main_window.table.item(row, 6).text()       # 원본 위치


            # 썸네일 위젯에서 jpg 경로 추출 (toolTip에 저장해두었다면)
            thumb_label = self.main_window.table.cellWidget(row, 1)
            thumb_path = thumb_label.toolTip() if thumb_label else None
            project = self.get_selected_project()
            if not project:
                print(" 프로젝트가 선택되지 않았습니다.")
                return

            base_dir = f"/home/rapa/show/{project['name']}"
            structure = create_plate_structure(
                base_dir=base_dir,
                shot_name=shot,
                plate_type=plate_type,
                version=version
            )
            # 1. 원본 복사
            for file in os.listdir(src_path):
                if file.lower().endswith((".exr", ".mov", ".mp4")):
                    shutil.copy2(os.path.join(src_path, file), structure["org"])

            # 2. 썸네일 복사 (jpg)
            if thumb_path and os.path.exists(thumb_path):
                shutil.copy2(thumb_path, os.path.join(structure["jpg"], os.path.basename(thumb_path)))

            # 3. 변환 대상 MOV 찾기
            input_video = None
    

            # 1. MOV/MP4가 있으면 우선
            for file in os.listdir(structure["org"]):
                if file.lower().endswith((".mov", ".mp4")):
                    input_video = os.path.join(structure["org"], file)
                    break

            # 2. 없으면 EXR 첫 프레임을 사용 (단일 프레임 기준)
            if not input_video:
                for file in sorted(os.listdir(structure["org"])):
                    if file.lower().endswith(".exr"):
                        input_video = os.path.join(structure["org"], file)
                        break
            
            # 여기 성형한다
            # 3. 이제 변환 시작
            if input_video:
                print(f" 변환 대상 파일: {input_video}")
                version_dir = os.path.dirname(structure["org"]) 
                mp4_path = os.path.join(version_dir, f"{shot}_plate_{version}.mp4")
                webm_path = os.path.join(version_dir, f"{shot}_plate_{version}.webm")
                montage_path = os.path.join(structure["montage"], f"{shot}_plate_{version}.jpg")


                mp4_ok = convert_to_mp4(input_video, mp4_path)
                webm_ok = convert_to_webm(input_video, webm_path)
                montage_ok = generate_montage_multi(
                    input_video,
                    output_dir=structure["montage"],
                    basename=shot,
                    interval=5,
                    max_frames=10
                )

                print(f"  MP4     : {'O' if mp4_ok else 'X'} → {mp4_path}")
                print(f"  WebM    : {'O' if webm_ok else 'X'} → {webm_path}")
                print(f"  Montage : {'O' if montage_ok else 'X'} → {montage_path}")
            else:
                print(f" {shot} → 변환할 MOV/MP4/EXR 파일이 org 폴더에 없습니다.")

        #샷그리드

    def on_register_to_shotgrid(self):


        # 프로젝트 선택
        project = self.get_selected_project()
        if not project:
            QtGui.QMessageBox.warning(self.main_window, "오류", "프로젝트가 선택되지 않았습니다.")
            return
        project_name = project["name"]

        # 샷 폴더 선택
        scan_root = f"/home/rapa/show/{project_name}/product/scan"
        selected_folder = QtGui.QFileDialog.getExistingDirectory(
            self.main_window,
            "샷 폴더 선택 (scanlist 있는 폴더)",
            scan_root
        )

        if not selected_folder:
            print(" 폴더 선택이 취소되었습니다.")
            return

        #  선택한 폴더에서 scanlist 엑셀 자동 찾기
        excel_files = [f for f in os.listdir(selected_folder) if f.startswith("scanlist") and f.endswith(".xlsx")]
        if not excel_files:
            QtGui.QMessageBox.warning(self.main_window, "오류", "선택한 폴더에 scanlist 엑셀이 없습니다.")
            return

        #  가장 최신 버전 엑셀 사용
        excel_files.sort()
        excel_path = os.path.join(selected_folder, excel_files[-1])

        print(f" 선택된 엑셀 파일: {excel_path}")

        # 4 0n_collect 호출
        self.on_collect()

        # 엑셀 로딩 후 ShotGrid 업로드 (기존 코드 흐름 사용)
        data_list = load_excel_data(excel_path)
        sg = connect_to_shotgrid()
        for data in data_list:
            shot_name = data["Shot Name"]
            version = data["Version"]
            type_ = data["Type"]

            # 현재 선택된 프로젝트 기준으로 직접 경로 재구성
            selected_project = self.get_selected_project()
            if not selected_project:
                print("X 프로젝트가 선택되지 않았습니다.")
                return
            project_name = selected_project["name"]

            base_path = f"/home/rapa/show/{project_name}/{shot_name}/plate/{type_}/{version}"

            mp4_path = os.path.join(base_path, f"{shot_name}_plate_{version}.mp4")
            webm_path = os.path.join(base_path, f"{shot_name}_plate_{version}.webm")
            montage_dir = os.path.join(base_path, "montage")
            montage_path = find_thumbnail_from_montage(montage_dir)

            # 썸네일은 여전히 엑셀에서 가져와도 되고, montage 썸네일로 대체해도 됨
            thumbnail_path = montage_path  # 또는 data.get("Thumbnail Path", "")

            # Shot 생성 및 등록
            project, shot = find_shot(sg, project_name, shot_name)
            if not shot:
                shot = create_shot(sg, project, shot_name, thumbnail_path)

            create_version(
                sg, project, shot, version,
                mp4_path=mp4_path,
                thumbnail_path=thumbnail_path,
                webm_path=webm_path,
                montage_path=montage_path
            )

        
    #UI 내 프로젝트 선택함수
    def select_project(self):
        sg = connect_to_shotgrid()
        projects = list_projects(sg)
        project_names = [p["name"] for p in projects]

        project_name, ok = QtGui.QInputDialog.getItem(
            self.main_window,
            "프로젝트 선택",
            "ShotGrid 프로젝트를 선택하세요:",
            project_names,
            editable=False
        )

        if ok and project_name:
            selected = next(p for p in projects if p["name"] == project_name)
            # 라벨에 표시
            self.main_window.project_label.setText(f"🔘 선택된 프로젝트: {project_name}")
            return selected
        else:
            self.main_window.project_label.setText(f"🛑 선택된 프로젝트: 없음")
            return None
        

    # 프로젝트에 불러와 콤보박스 세팅
    def load_shotgrid_projects(self):
        sg = connect_to_shotgrid()
        self.projects = list_projects(sg)

        self.main_window.project_combo.clear()
        for project in self.projects:
            self.main_window.project_combo.addItem(project["name"])

    

    # 선택된 프로젝트 가져오는 함수
    def get_selected_project(self):
        name = self.main_window.project_combo.currentText()
        selected = next((p for p in self.projects if p["name"] == name), None)
        return selected
    
    # 업로드 시 선택된 프로젝트 사용
    def on_register_from_selected_excel(self):
        selected_excel = self.on_select_excel_version()
        if not selected_excel:
            return

        selected_project = self.get_selected_project()
        if not selected_project:
            print("X 프로젝트가 선택되지 않았습니다.")
            return
        
    # 모든 체크박스 선택 / 해제
    def select_all_rows(self):
        row_count = self.main_window.table.rowCount()
        for row in range(row_count):
            checkbox = self.main_window.table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(True)
        print(f"✔ {row_count}개 항목 모두 체크됨")

    def toggle_select_all(self):
        row_count = self.main_window.table.rowCount()
        new_state = not self.select_all_checked  # True → 체크, False → 해제

        for row in range(row_count):
            checkbox = self.main_window.table.cellWidget(row, 0)
            if checkbox:
                checkbox.setChecked(new_state)

        # 버튼 텍스트 업데이트
        if new_state:
            self.main_window.toggle_select_button.setText("모두 해제")
            print(f"{row_count}개 항목 전체 선택됨")
        else:
            self.main_window.toggle_select_button.setText("모두 선택")
            print(f"전체 해제됨")

        self.select_all_checked = new_state

    def update_project_label(self, project_name):
        if project_name:
            self.main_window.project_label.setText(f"🔘 선택된 프로젝트: {project_name}")
        else:
            self.main_window.project_label.setText("🛑 선택된 프로젝트: 없음")

    

    # def __init__(self):
    #     """
    #     Constructor
    #     """
    #     # first, call the base class and let it do its thing.
    #     QtGui.QWidget.__init__(self)

    #     # now load in the UI that was created in the UI designer
    #     self.ui = main()
    #     main(self)

    #     # most of the useful accessors are available through the Application class instance
    #     # it is often handy to keep a reference to this. You can get it via the following method:
    #     self._app = sgtk.platform.current_bundle()

    #     # logging happens via a standard toolkit logger
    #     logger.info("Launching Scandata Converter Application...")

    #     # via the self._app handle we can for example access:
    #     # - The engine, via self._app.engine
    #     # - A Shotgun API instance, via self._app.shotgun
    #     # - An Sgtk API instance, via self._app.sgtk

    #     # lastly, set up our very basic UI
    #     self.ui.context.setText("Current Context: %s" % self._app.context)
