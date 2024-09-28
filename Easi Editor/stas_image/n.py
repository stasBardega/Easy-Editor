from PyQt5.QtCore import*
from PyQt5.QtWidgets import*
import os

app = QApplication([])
win = QWidget()
win.resize(700, 500)
win.setWindowTitle("Easy Editor")

btn_file = QPushButton("Папка")
btn_left = QPushButton("Ліворуч")
btn_right = QPushButton("Праворуч")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_blur = QPushButton("Розмиття")
btn_black_white = QPushButton("Ч/Б")

list_file = QListWidget()
lbl_picture = QLabel("Картинка")

#Макет
v1 = QVBoxLayout()
v2 = QVBoxLayout()

h1 = QHBoxLayout()
h2 = QHBoxLayout()

main_layout = QHBoxLayout()

v1.addWidget(btn_file)
v1.addWidget(list_file)

h1.addWidget(btn_left)
h1.addWidget(btn_right)
h1.addWidget(btn_mirror)
h1.addWidget(btn_sharp)
h1.addWidget(btn_black_white)

h2.addWidget(btn_blur)

v2.addWidget(lbl_picture)
v2.addLayout(h1)
v2.addLayout(h2)

main_layout.addLayout(v1)
main_layout.addLayout(v2)

win.setLayout(main_layout)

#Завдання 2
#Зберігаємо шлях до вказаної папки
workdir = ""


# - вибирати робочу папку
def chooseWorkdir():
    global workdir
    workdir = QFileDialog.getExistingDirectory() # - запитуємо у діалоговому вікні  

# - фільтрувати файли
def filter(filenames, extensions):
    result = []                                  # список для зберігання назв файлів
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)

    return result

#Відбір файлів та відображення їх у віджет
def showFilenamesList():
    chooseWorkdir()
    extensions = [".jpg",".png",".jpeg",".gif",".bmp"]
    filenames = filter(os.listdir(workdir),extensions)
    list_file.clear()
    for file in filenames:
        list_file.addItem(file)



btn_file.clicked.connect(showFilenamesList)



win.show()
app.exec_()