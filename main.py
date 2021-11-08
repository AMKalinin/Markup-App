import os

from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


import second_form


class MainWindow(QMainWindow):

    def __init__(self):

        self.color = [QColor.fromRgb(255,0,0,100), QColor.fromRgb(255,255,0,100), QColor.fromRgb(0,0,255,100), 
                        QColor.fromRgb(0,130,50,150),QColor.fromRgb(0,255,0,150),QColor.fromRgb(127,255,212,100),
                        QColor.fromRgb(68,148,74,100),QColor.fromRgb(249,132,229,100),QColor.fromRgb(189,51,164,100)]
        self.mask = [[],[]]
        self.chosen_points = []
        self.class_list = [[]] 

        QMainWindow.__init__(self)
        loadUi('main.ui', self)
        self.setWindowTitle('Markup')


        self.pushButton_open.clicked.connect(self.addImages)
        self.pushButton_save_mask.clicked.connect(self.save_mask)
        self.pushButton_save.clicked.connect(self.save)
        self.listImage.itemClicked.connect(self.selectionChenged)
        self.pushButton_class.clicked.connect(self.add_class)

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
        xy = cursor_event.pos()
        if (xy.x()>self.toolBar.width()) and (xy.y()> self.statusbar.height()):
            if (xy.x()<self.pix2.width()) and (xy.y()< self.pix2.height()):
                xy.setX(xy.x()-self.toolBar.width())
                xy.setY(xy.y() - self.statusbar.height())
                self.chosen_points.append(xy)
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
            
            painter.drawLine(self.chosen_points[-2],self.chosen_points[-1])

            painter.end()
            self.label.setPixmap(self.pix)

    def getCode(self, name):
        try:
            a = self.sec_win.class_list.loc[self.sec_win.class_list['type'] == name].values[0][-1]
        except:
            a = self.sec_win.class_list.loc[self.sec_win.class_list['type2'] == name].values[0][-1]
        return a


    # Сохранение класса и координат маски
    def save_mask(self):
        self.mask[0].append(self.getCode(self.listClass.currentItem().data(0)))
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

    # Вызов формы с существующими классами
    def add_class(self):
        self.sec_win = second_form.SecondWindow(self)
        self.listClass.clear()
        self.sec_win.table = self.listClass
        self.sec_win.show()


app = QApplication([])
window = MainWindow()
window.show()
app.exec_()