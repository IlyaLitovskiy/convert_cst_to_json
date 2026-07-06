import sys
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QComboBox, QLabel, QFileDialog
import pandas as pd
import os
import csv
import json

class Window(QWidget):
    def __init__(self):
        super().__init__()
        #Глобальные переменные для хранения состояний
        self.source_path = None
        self.convert_mode = 0 #Еслил 0 то режим CSV -> JSON, иначе JSON -> CSV
        self.source_extensiont = None #Формат файла
        self.file_size = 0 #Размер файла

        #Главное окно
        self.setStyleSheet("background-color: gray")
        self.setWindowTitle("Конвертер файлов")
        self.resize(500, 600)

        #Кнопки
        self.button_open_file = QPushButton("Загрузить файл", self)
        self.button_open_file.resize(500, 25)
        self.button_open_file.move(0, 0)
        self.button_save_file = QPushButton("Сохранить как", self)
        self.button_save_file.resize(500, 25)
        self.button_save_file.move(0, 70)

        #Выпадающий список
        self.combobox = QComboBox(self)
        self.combobox.addItem("CSV -> JSON")
        self.combobox.addItem("JSON -> CSV")
        self.combobox.resize(500, 25)
        self.combobox.move(0,35)

        self.button_open_file.clicked.connect(self.open_file)
        self.combobox.currentTextChanged.connect(self.convert_file_mod)
        self.button_save_file.clicked.connect(self.save_file)

        self.show()

    def open_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите файл",
            "D:/PythonStepik/test_dock",
            "Csv файлы (*.csv);;Json файлы (*.json)"
        )

        if not file_path:
            print("Выбор файла отменён")
            return

        self.source_path = file_path
        self.source_extensiont = os.path.splitext(file_path)[1]

        self.file_size = os.path.getsize(self.source_path)
        if self.file_size == 0:
            print("Выбранный файл пуст!")

    def convert_file_mod(self):
        if self.combobox.currentText() == "CSV -> JSON":
            self.convert_mode = 0
        else:
            self.convert_mode = 1

    def save_file(self):
        if self.source_path is None:
            print("Файл не выбран!")
            return

        if self.convert_mode == 0:  # конвертация CSV -> JSON
            if self.source_extensiont != ".csv":
                print("Ошибка: при выбранном режиме CSV -> JSON, загружается файл формата не являющийся .csv")
                return

            default_conv = ".json"
            file_filter = "JSON файлы (*.json)"
            convert_function = self.convert_csv_to_json
        else: # конвертация JSON -> CSV
            if self.source_extensiont != ".json":
                print("Ошибка: при выбранном режиме JSON -> CSV, загружается файл формата не являющийся .json")
                return
            default_conv = ".csv"
            file_filter = "CSV файлы (*.csv)"
            convert_function = self.convert_json_to_csv

        #Окно проводника для сохранения файла
        save_path, _ = QFileDialog.getSaveFileName(
            self,
            "Сохранить как",
            os.path.dirname(self.source_path) + "/converted" + default_conv,
            file_filter
        )
        if not save_path:
            print("Сохранение отменено")
            return

        # Выполняем конвертацию
        try:
            convert_function(save_path)
            print(f"Файл успешно сохранён: {save_path}")
        except Exception as error:
            print(f"Ошибка конвертации: {error}")

    #Ф-ция конвертации из CSV в JSON
    def convert_csv_to_json(self, out_path):
        df = pd.read_csv(self.source_path)
        df.to_json(out_path, orient='records', lines=True, force_ascii=False)

    #Ф-ция конвертации из JSON в CSV
    def convert_json_to_csv(self, out_path):
        df = pd.read_json(self.source_path, orient='records', lines=True)
        df.to_csv(out_path, index=False, encoding='utf-8-sig')

path_for_gen_data = "D:/PythonStepik/test_dock"
csv_gen_path = os.path.join(path_for_gen_data, "firstdataforcsv.csv")
join_gen_path = os.path.join(path_for_gen_data, "firstdataforjson.json")

#Генерация файла с данными для .csv
dataforcsv = [
        [1231341],
        [5875394085],
        [42342024279364]
]
with open(csv_gen_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerows(dataforcsv)

#Генерация файла с данными для .json
dataforjson = [
    {"Ананас": 1231341},
    {"Апельсин": 5875394085},
    {"Алыча": 42342024279364}
]
with open(join_gen_path, 'w', encoding='utf-8') as jsonfile:
    for item in dataforjson:
        jsonfile.write(json.dumps(item, ensure_ascii=False) + '\n')

app = QApplication(sys.argv)
Window = Window()
sys.exit(app.exec())