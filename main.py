import sqlite3
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QTableWidgetItem
from PyQt5.uic.properties import QtWidgets

from form import Ui_Form
from med import Ui_MainWindow


class Form(QWidget):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.main_window = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.dateTimeEdit.setCalendarPopup(True)
        self.ui.pushButton.clicked.connect(self.add_patient)

    def add_patient(self):
        values_list = [
            self.ui.lineEdit.text(),  # ФИО
            self.ui.dateTimeEdit.text(),  # Дата и время
            self.ui.lineEdit_3.text(),  # Возраст
            self.ui.lineEdit_4.text(),  # Адрес
            self.ui.lineEdit_5.text(),  # Номер ЧД
            self.ui.comboBox.currentText(),  # Значение avpu
            self.ui.lineEdit_8.text(),  # Значение spo2
            self.ui.comboBox_2.currentText()  # Значение aries_affect
        ]
        sum_bal = self.calculate_sum_bal()

        # Determine the target table based on sum_bal
        if sum_bal > 21:
            target_table = self.main_window.tableWidget_4
        elif 16 <= sum_bal <= 21:
            target_table = self.main_window.tableWidget_5
        elif 6 <= sum_bal <= 15:
            target_table = self.main_window.tableWidget_6
        elif 0 <= sum_bal <= 5:
            target_table = self.main_window.tableWidget_7

        # Add the values to the target table
        row_position = target_table.rowCount()
        target_table.insertRow(row_position)
        for column, item in enumerate(values_list):
            target_table.setItem(row_position, column, QTableWidgetItem(str(item)))

    def calculate_sum_bal(self):
        sum_bal = 0
        ad = self.ui.lineEdit_4.text()
        if ad.isdigit():
            value = int(ad)
            if value >= 90:
                sum_bal += 4
            elif 76 <= value <= 89:
                sum_bal += 3
            elif 50 <= value <= 75:
                sum_bal += 2
            elif 1 <= value <= 49:
                sum_bal += 1

        chd = self.ui.lineEdit_5.text()
        if chd.isdigit():
            value1 = int(chd)
            if 10 <= value1 <= 30:
                sum_bal += 4
            elif value1 > 30:
                sum_bal += 3
            elif 6 <= value1 <= 9:
                sum_bal += 2
            elif 1 <= value1 <= 5:
                sum_bal += 1

        avpu = self.ui.comboBox.currentIndex()
        if avpu == 0:
            sum_bal += 4
        elif avpu == 1:
            sum_bal += 3
        elif avpu == 2:
            sum_bal += 2
        elif avpu == 3:
            sum_bal += 1

        spo2 = self.ui.lineEdit_8.text()
        if spo2.isdigit():
            value2 = int(spo2)
            if value2 > 96:
                sum_bal += 4
            elif 94 <= value2 <= 96:
                sum_bal += 3
            elif 90 <= value2 <= 94:
                sum_bal += 2
            elif value2 < 90:
                sum_bal += 1

        aries_affect = self.ui.comboBox_2.currentIndex()
        if aries_affect == 0:
            sum_bal += 6
        elif aries_affect == 1:
            sum_bal += 4
        elif aries_affect == 2:
            sum_bal += 3
        elif aries_affect == 3:
            sum_bal += 1

        return sum_bal


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
