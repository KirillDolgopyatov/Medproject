import sys  # Импорт системного модуля

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget

from form import Ui_Form
from med import Ui_MainWindow  # Импорт дизайна интерфейса, созданного в Qt Designer


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)


class MainWindow(QMainWindow):  # Определение класса MainWindow, наследующего QMainWindow
    def __init__(self):
        super().__init__()  # Вызов конструктора базового класса
        self.login_form = None
        self.ui = Ui_MainWindow()  # Создание экземпляра дизайна интерфейса
        self.ui.setupUi(self)  # Настройка интерфейса в текущем окне

        self.ui.pushButton.clicked.connect(self.openLoginForm)

    def openLoginForm(self):
        self.login_form = Form()
        self.login_form.show()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
