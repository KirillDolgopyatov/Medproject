import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget
from PyQt5.uic.properties import QtWidgets

from form import Ui_Form
from med import Ui_MainWindow


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.ui.dateTimeEdit.setCalendarPopup(True)
        self.ui.pushButton.clicked.connect(self.add_patient)

    def add_patient(self):
        pass


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.login_form = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.pushButton.clicked.connect(self.openLoginForm)

        self.conn = sqlite3.connect('patients_data.db')
        self.cursor = self.conn.cursor()

        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_I (id INTEGER PRIMARY KEY, ФИО TEXT, Дата поступления TEXT, 
            Возраст TEXT, АД TEXT, ЧД TEXT, ШГ TEXT, SpO2 TEXT, Оп TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_II (id INTEGER PRIMARY KEY,ФИО TEXT, Дата поступления TEXT, 
            Возраст TEXT, АД TEXT, ЧД TEXT, ШГ TEXT, SpO2 TEXT, Оп TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_III (id INTEGER PRIMARY KEY, ФИО TEXT, Дата поступления TEXT, 
            Возраст TEXT, АД TEXT, ЧД TEXT, ШГ TEXT, SpO2 TEXT, Оп TEXT)''')
        self.cursor.execute(
            '''CREATE TABLE IF NOT EXISTS table_IV (id INTEGER PRIMARY KEY, ФИО TEXT, Дата поступления TEXT, 
            Возраст TEXT, АД TEXT, ЧД TEXT, ШГ TEXT, SpO2 TEXT, Оп TEXT)''')
        self.conn.commit()

        self.load_data_from_sqlite()

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

    def load_data_from_sqlite(self):
        # Подключение к базе данных
        connection = sqlite3.connect('patients_data.db')
        cursor = connection.cursor()

        # Словарь для сопоставления имен таблиц с виджетами таблиц в UI
        table_widgets = {
            'table_I': self.ui.tableWidget_4,
            'table_II': self.ui.tableWidget_5,
            'table_III': self.ui.tableWidget_6,
            'table_IV': self.ui.tableWidget_7,
        }

        for table_name, table_widget in table_widgets.items():
            cursor.execute(f"SELECT * FROM {table_name}")
            rows = cursor.fetchall()
            table_widget.setRowCount(0)  # Очистка таблицы перед заполнением

            for row in rows:
                row_position = table_widget.rowCount()
                table_widget.insertRow(row_position)
                for column, item in enumerate(row):
                    table_widget.setItem(row_position, column, QtWidgets.QTableWidgetItem(str(item)))

        # Закрытие соединения с базой данных
        connection.close()

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
