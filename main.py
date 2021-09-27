import os
import random 

from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self):

        self.color = [QColor.fromRgb(255,0,0,100), QColor.fromRgb(255,255,0,100), QColor.fromRgb(0,0,255,100), 
                        QColor.fromRgb(0,0,0,150),QColor.fromRgb(0,255,0,150),QColor.fromRgb(127,255,212,100),
                        QColor.fromRgb(68,148,74,100),QColor.fromRgb(249,132,229,100),QColor.fromRgb(189,51,164,100)]
        self.mask = [[],[]]
        self.chosen_points = []
        self.class_list = []


        QMainWindow.__init__(self)

        loadUi("forma.ui", self)

        self.setWindowTitle("proga")

        self.create_file()
        self.add_classes()

        self.pushButton_open.clicked.connect(self.addImages)

        self.pushButton_save_mask.clicked.connect(self.save_mask)
        self.pushButton_save.clicked.connect(self.save)
        self.pushButton_addClass.clicked.connect(self.addClass)

        self.listImage.itemClicked.connect(self.selectionChenged)

    # добавление списка файлов в Qlist
    def addImages(self):
        list_images = self.getFileNames()[0]
        self.listImage.addItems(list_images)

    # Получение списка файлов
    def getFileNames(self):
        file_filter = 'JPEG File (*.jpeg);; JPG File (*.jpg);; PNG File (*.png);; All Files (*.*) '
        response = QFileDialog.getOpenFileNames(
            parent = self,
            caption = 'Select',
            directory = os.getcwd(),
            filter = file_filter,
            initialFilter = 'All Files (*.*)'
        )
        return response

    # для отображения файла выбранного из списка
    def selectionChenged(self, item):
        self.pix = QPixmap(item.text())#.scaled(600, 600)
        self.pix2 = QPixmap(item.text())

        painter = QPainter()
        painter.begin(self.pix2)

        pen = QBrush(Qt.black)

        painter.setBrush(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawRect(0,0,self.pix2.width(), self.pix2.height())
        painter.end()

        self.label.setPixmap(self.pix)

        self.chosen_points = []

    # Получение координат клика
    def mouseReleaseEvent(self, cursor_event):
        self.chosen_points.append(cursor_event.pos())
        self.update()

    # Отрисовка линий по нажатым точкам на нашем изображении
    def paintEvent(self, paint_event):
        if len(self.chosen_points)>1:
            #self.label.clear()

            painter = QPainter()


            painter.begin(self.pix)

            #painter.drawPixmap(0, 0, self.pix)

            color_index = self.listClass.currentRow()

            pen = QPen(self.color[color_index], 1, Qt.SolidLine)

            painter.setPen(pen)

            painter.setRenderHint(QPainter.Antialiasing, True)
            for i in range(len(self.chosen_points)-1):
                painter.drawLine(self.chosen_points[i],self.chosen_points[i+1])
            painter.end()
            self.label.setPixmap(self.pix)

    # Сохранение класса и координат маски
    def save_mask(self):
        self.mask[0].append(self.listClass.currentRow())
        self.mask[1].append(self.chosen_points)

        painter = QPainter()
        painter2 = QPainter()


        painter.begin(self.pix)
        painter2.begin(self.pix2)


        color_index = self.listClass.currentRow()

        pen = QBrush(self.color[color_index])
        pen2 = QBrush(self.color[color_index])
        painter2.setBrush(pen2)

        painter.setBrush(pen)
        painter.setRenderHint(QPainter.Antialiasing, True)
        painter.drawPolygon(*self.chosen_points)
        painter2.drawPolygon(*self.chosen_points)

        painter.end()
        painter2.end()
        self.label.setPixmap(self.pix)

        self.chosen_points = []

    # Запись в файлы изображения с маской и текстового файла с значением класса и координатами
    def save(self):
        filePath, _= QFileDialog.getSaveFileName(self,"Save Image", "", "PNG(*.png)")
        if filePath =="":
            return

        self.pix2.save(filePath)

        filePath = filePath[:-4]+'.txt'
        f = open(filePath, 'w')
        for i in range(len(self.mask[0])):
            f.write(str(self.mask[0][i])+' ')
            for j in range(len(self.mask[1][i])):
                f.write(str(self.mask[1][i][j].x()) + ' ' + str(self.mask[1][i][j].y()) + ' ')
            f.write('\n')
        f.close()

        self.mask = [[],[]]

    # Добавление классов в Qlist
    def addClass(self):
        f = open('Classes.txt', 'a')
        clas = str(len(self.class_list)+1) + ' ' + self.lineEdit_class.text()+ ' ' + '\n'
        f.write(clas)
        f.close()
        self.class_list.append(clas)
        self.listClass.addItem(self.lineEdit_class.text())

    # Создание файла с классами
    def create_file(self):
        f = open('Classes.txt', 'a')
        f.close()
    
    # Добавление существующих классов в список
    def add_classes(self):
        f = open('Classes.txt', 'r')
        for line in f:
            clas = line.split(' ')
            self.listClass.addItem(clas[1])
            self.class_list.append(clas)
        f.close()








app = QApplication([])
window = MainWindow()
window.show()
app.exec_()