# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'dialog.ui'
#
# Created: Fri Jul 10 15:44:44 2020
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

# from sgtk.platform.qt import (
#     QWidget, QLabel, QPushButton, QTableWidget, QVBoxLayout,
#     QHBoxLayout, QFileDialog, QTableWidgetItem, QCheckBox, QComboBox
# )
# from sgtk.platform.qt import QPixmap

from tank.platform.qt import QtCore
for name, cls in QtCore.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls

from tank.platform.qt import QtGui
for name, cls in QtGui.__dict__.items():
    if isinstance(cls, type): globals()[name] = cls
    
from  . import resources_rc




class Ui_Dialog(object):
    # def __init__(self):
    def setupUi(self, Dialog):

        Dialog.setWindowTitle("ScanData Converter")
        Dialog.resize(1200, 800)
        # super().__init__()
        # self.setWindowTitle("ScanData IO Manager")
        # self.setMinimumSize(1200, 800)

        # ==== 위쪽: 경로 및 버튼 ====
        self.path_label = QtGui.QLabel(" 경로를 선택하세요")
        self.select_button = QtGui.QPushButton("Select")
        self.load_button = QtGui.QPushButton("Load")

        path_layout = QtGui.QHBoxLayout()
        path_layout.addWidget(QtGui.QLabel("Path:"))
        path_layout.addWidget(self.path_label)
        path_layout.addWidget(self.select_button)
        path_layout.addWidget(self.load_button)

        # ==== 중간: 테이블 ====
        self.table = QtGui.QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Check", "Thumbnail", "Roll", "Shot Name", "Version", "Type", "Path"
        ])

        # ==== 아래쪽: 액션 버튼 ====
        self.save_button = QtGui.QPushButton("Save Excel")

        bottom_layout = QtGui.QHBoxLayout()
        bottom_layout.addWidget(self.save_button)


        # 체크박스 모두 선택 / 해제 

        self.toggle_select_button = QtGui.QPushButton("모두 선택")
        bottom_layout.addWidget(self.toggle_select_button)


        # 엑셀 선택하여 샷그리드에 바로 업로드
        self.register_excel_button = QtGui.QPushButton("엑셀 선택 → ShotGrid 업로드")
        bottom_layout.addWidget(self.register_excel_button)



        # 프로젝트에 바로 뜨도록 하기 
        self.project_label = QtGui.QLabel("🔘 선택된 프로젝트: 없음")
        bottom_layout.addWidget(self.project_label)


        # 프로젝트 선택 UI
        self.project_combo_label = QtGui.QLabel("프로젝트 선택:")
        self.project_combo = QtGui.QComboBox()
        # 초기화 시 기본값
        self.project_combo.addItem("ShotGrid 프로젝트 불러오는 중...")

        # 위쪽레이아웃에 추가
        top_layout = QtGui.QHBoxLayout()
        top_layout.addWidget(self.project_combo_label)
        top_layout.addWidget(self.project_combo)

        # ==== 전체 레이아웃 ====
        layout = QtGui.QVBoxLayout()
        layout.addLayout(top_layout)
        layout.addLayout(path_layout)
        layout.addWidget(self.table)
        layout.addLayout(bottom_layout)
        self.setLayout(layout)

    def set_path(self, path):
        self.path_label.setText(path)

    def add_table_row(self, data, row=None):
        if row is None:
            row = self.table.rowCount()
        self.table.insertRow(row)

        # CheckBox
        checkbox = QtGui.QCheckBox()
        self.table.setCellWidget(row, 0, checkbox)

        # 썸네일 셀 (예시)
        thumb_label = QtGui.QLabel()
        pixmap = QtGui.QPixmap(data["thumbnail"])
        if not pixmap.isNull():
            thumb_label.setPixmap(pixmap.scaled(100, 60))
            thumb_label.setToolTip(data["thumbnail"])
        else:
            thumb_label.setText("❌")
        self.table.setCellWidget(row, 1, thumb_label)
        thumb_label.setToolTip(data["thumbnail"]) 

        # 나머지 데이터
        self.table.setItem(row, 2, QtGui.QTableWidgetItem(data["roll"]))
        self.table.setItem(row, 3, QtGui.QTableWidgetItem(data["shot_name"]))
        self.table.setItem(row, 4, QtGui.QTableWidgetItem(data["version"]))
        self.table.setItem(row, 5, QtGui.QTableWidgetItem(data["type"]))
        self.table.setItem(row, 6, QtGui.QTableWidgetItem(data["path"]))

