# main.py

import sys
from PySide6.QtWidgets import QApplication, QWidget
from .controller import Controller
from .main_window import MainWindow


# def main():
#     print(" io_main.py 내부의 main() 함수가 실행되었습니다.")

#     app = QApplication(sys.argv)
        
#     controller = Controller()  # 컨트롤러가 UI와 로직을 묶어줌
#     controller.show_main_window()
        
#     sys.exit(app.exec())

def main():
    print(" io_main.py 내부의 main() 함수가 실행되었습니다.")

    app = QApplication(sys.argv)
    if app is None:
        print(" Qt 앱 없음, 새로 생성")
        import sys
        app = QApplication(sys.argv)

    win = QWidget()
    win.setWindowTitle("ScanData Converter")
    win.resize(400, 200)
    win.show()
    print(" 윈도우 show() 호출됨")  

    controller = Controller()  # 컨트롤러가 UI와 로직을 묶어줌
    controller.show_main_window()
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
