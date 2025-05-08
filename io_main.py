# main.py

import sys
from PySide6.QtWidgets import QApplication
from controller import Controller
from main_window import MainWindow


def main():
    print("io_main.py 내부의 main() 함수가 실행되었습니다.")

    app = QApplication(sys.argv)
        
    controller = Controller()  # 컨트롤러가 UI와 로직을 묶어줌
    controller.show_main_window()
        
    sys.exit(app.exec())

if __name__ == "__main__":
    main()



# from controller import Controller
# from main_window import MainWindow


# def main():
#     print("io_main.py 내부의 main() 함수가 실행되었습니다.")
#     print("▶ main() 진입")

#     controller = Controller()
#     controller.show_main_window()