# - підключення модулів
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
import os

from PIL import Image,ImageFilter

# - об'єкт-додаток та вікно програми.
app = QApplication([])

win = QWidget()
win.resize(700,500)
win.setWindowTitle('Easy Editor')
win.show()

# Віджети - кнопки, надписи та список
btn_file = QPushButton("Папка")
btn_left = QPushButton("Ліворуч")
btn_right = QPushButton("Праворуч")
btn_mirror = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_blur = QPushButton("Розмиття")
btn_black_white = QPushButton("Ч/Б")

lbl_picture = QLabel("Картинка")

list_file = QListWidget()        # список віддетів


# Макет - Лінії
v1 = QVBoxLayout()
v2 = QVBoxLayout()
h1 = QHBoxLayout()
h2 = QHBoxLayout()
main_layout = QHBoxLayout()

v1.addWidget(btn_file)         # у першому – кнопка вибору директорії та список файлів
v1.addWidget(list_file)

h1.addWidget(btn_left)         # кнопки з фільтрами
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

# -                                                                   [ Завдання №2 ]

# - змінна для збереження імені папки
workdir = ""

# - ---------------  функція вибору робочої папки
def chooseWorkgir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()

# - --------------- Функція відбору імен файлів розширень
def filter(filenames, extensions):
    result = []
    for filename in filenames:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result

# - --------------- Відповідає за вибір папки, відбір файлів та відображення їх у віджеті
def showfilenamesList():
    chooseWorkgir()
    extensions = ['.jpg','.jpeg', '.png', '.gif', '.bmp']
    filenames = filter(os.listdir(workdir), extensions)
    list_file.clear()
    for file in filenames:
        list_file.addItem(file)


# -                                                                 [ Завдання №3 ]

class ImageProcessor():

    def __init__(self):
        self.image = None               # поточне зображення, з яким працює програма.
        self.filename = None            # ім'я поточного зображення.
        self.dir = None                 # шлях до директорії з зображенням
        self.savedir = 'Modified/'      # папка, куди будуть зберігатися змінені зображення 


    # -                               завантаження картинки з папки за вибраним ім'ям у списку картинок
    def loadImage(self,filename,dir):
        self.filename = filename
        self.dir = dir
        image_path = os.path.join(dir,filename)   # Зі шляху до робочої папки та імені файлу сформуємо шлях до картинки
        self.image = Image.open(image_path)       # Відкриємо картинку (об'єкт Image), звернувшись за повним шляхом та зберігаємо в змінну зображення


    # -                             відображення поточного зображення у вікні програми
    def showImage(self):
        # Шлях до тимчасового зображення
        temp_image_path = os.path.join(workdir, self.savedir, self.filename)
        pixmapimage = QPixmap(temp_image_path)                               # - Повним шляхом до файлу створюємо об'єкт QPixmap спеціально для відображення графіки в інтерфейсі.
        w = lbl_picture.width()                                   # - Дізнаємося розміри поля для розміщення картинки
        h = lbl_picture.height()
        pixmapimage = pixmapimage.scaled(w,h,Qt.KeepAspectRatio)   # - Адаптуємо картинку під розміри поля
        lbl_picture.setPixmap(pixmapimage)                         # - Розміщуємо картинку у віджеті lb_image


    # -                              Збереження Картинки як файла в папку
    def saveImage(self):
        path = os.path.join(workdir, self.savedir)       # Формуємо шлях до папки для збереження

        if not os.path.exists(path):                     # Якщо  Папки для збереження ще немає (перевіряємо чи інснує)?
            os.mkdir(path)                                    # За сформованим шляхом створити нову папку

        image_path = os.path.join(path, self.filename)   # Формуємо шлях до картинки, що зберігається (з ім'ям файлу картинки!)
        self.image.save(image_path)                      # Зберігаємо картинку вбудованим методом класу Image



    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        self.showImage()


# - створення екземпляра класу
workimage = ImageProcessor()


# - яка отримує з віджету-списку ім'я вибраного файлу і відображає його у вікні програми
def showSelectImage():
    if list_file.selectedItems():
        filename = list_file.selectedItems()[0].text()
        workimage.loadImage(filename, workdir)
        workimage.saveImage()  # Зберігаємо одразу оригінальне зображення в директорію "Modified"
        workimage.showImage()  # Відображаємо зображення





# Підключення Функції до кнопок
btn_file.clicked.connect(showfilenamesList) # кнопка папка

list_file.itemClicked.connect(showSelectImage) # превю фотки

btn_black_white.clicked.connect(workimage.do_bw)



app.exec()