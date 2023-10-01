from PyQt6 import uic
from PyQt6.QtWidgets import QApplication
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QInputDialog, QFileDialog, QGridLayout, QLineEdit, QLabel
from pathlib import Path
import main_prog

Form, Window = uic.loadUiType("main_interface.ui")

app = QApplication([])
window = Window()
form = Form()
form.setupUi(window)
window.show()


def showFileDialog():
    '''options = QFileDialog.Options()
    options |= QFileDialog.DontUseNativeDialog'''
    directory = QFileDialog.getExistingDirectory(None, "Выбрать директорию", '/home')
    if directory:
        # передаем строку директории в главную функцию
        path = Path(directory)
        main_function(path)

def main_function(directory):
    form.label_2.setText(str(directory))
    print(f"Выбранная директория: {directory}")
    main_prog.main_prog(str(directory))

#form.label.setText()
form.toolButton.clicked.connect(showFileDialog)
form.progressBar.setProperty("value", 1)


app.exec()