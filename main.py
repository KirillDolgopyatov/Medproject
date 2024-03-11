import sqlite3
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

        self.conn = sqlite3.connect('patients_data.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_data_4 (id INTEGER PRIMARY KEY, column1 TEXT, column2 TEXT, 
            column3 TEXT, column4 TEXT, column5 TEXT, column6 TEXT, column7 TEXT, column8 TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_data_5 (id INTEGER PRIMARY KEY, column1 TEXT, 
            column2 TEXT, column3 TEXT, column4 TEXT, column5 TEXT, column6 TEXT, column7 TEXT, column8 TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_data_6 (id INTEGER PRIMARY KEY, column1 TEXT, 
            column2 TEXT, column3 TEXT, column4 TEXT, column5 TEXT, column6 TEXT, column7 TEXT, column8 TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_data_7 (id INTEGER PRIMARY KEY, column1 TEXT, 
            column2 TEXT, column3 TEXT, column4 TEXT, column5 TEXT, column6 TEXT, column7 TEXT, column8 TEXT)''')
        self.conn.commit()

    def save_table_data(self, tableWidget, table_name):
        rowCount = tableWidget.rowCount()
        columnCount = tableWidget.columnCount()
        for row in range(rowCount):
            row_data = []
            for column in range(columnCount):
                item = tableWidget.item(row, column)
                if item is not None:  # Проверяем, есть ли элемент
                    row_data.append(item.text())
                else:
                    row_data.append("")
            # Сохраняем строку данных в базу данных
            placeholders = ', '.join(['?'] * len(row_data))
            self.cursor.execute(f"INSERT INTO {table_name} VALUES (NULL, {placeholders})", row_data)
        self.conn.commit()

    def openLoginForm(self):
        self.login_form = Form()
        self.login_form.show()

    def closeEvent(self, event):
        self.save_table_data(self.ui.tableWidget_4, 'table_data_4')
        self.save_table_data(self.ui.tableWidget_5, 'table_data_5')
        self.save_table_data(self.ui.tableWidget_6, 'table_data_6')
        self.save_table_data(self.ui.tableWidget_7, 'table_data_7')
        self.conn.close()
        super().closeEvent(event)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
