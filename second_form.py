from PyQt5.QtWidgets import*
from PyQt5.uic import loadUi

import pandas as pd

class SecondWindow(QWidget):
    def __init__(self, parent=None):
        
        self.table = []
        super().__init__(parent)
        loadUi('second_form.ui', self)
        self.class_list =  pd.read_csv('Classes.csv')
        self.add()
        self.cods = {}

        self.pushButton_cancel.clicked.connect(self.cancel)
        self.pushButton_add.clicked.connect(self.add_in_list)

    def cancel(self):
        self.close()
        

    def add_in_list(self):
        a = self.tableWidget.selectedIndexes()
        for i in range(len(a)):
            self.table.addItem(a[i].data())        
        self.close()
        
    def add(self):
        headers = self.class_list.columns.values.tolist()
        self.tableWidget.setColumnCount(len(headers))
        self.tableWidget.setHorizontalHeaderLabels(headers)
        ind_row = 'NaN'
        ind_konec = 0

        ind_row1 = 'NaN'

        for i, row in self.class_list.iterrows():    
        # Добавление строки
            self.tableWidget.setRowCount(self.tableWidget.rowCount() + 1)
            ind_konec = i
            if ind_row == 'NaN':
                name = str(row[0])
                ind_row = i
            
            if (name != str(row[0])) or (i==self.tableWidget.rowCount()):
                name = str(row[0])
                self.tableWidget.setSpan(ind_row,0,i-ind_row,1)
                ind_row = i


            if ind_row1 == 'NaN':
                name1 = str(row[1])
                ind_row1 = i
            
            if (name1 != str(row[1])) or (i==self.tableWidget.rowCount()) :
                name1 = str(row[1])
                self.tableWidget.setSpan(ind_row1,1,i-ind_row1,1)
                ind_row1 = i

            for j in range(self.tableWidget.columnCount()):
                self.tableWidget.setItem(i, j, QTableWidgetItem(str(row[j])))
        
        self.tableWidget.setSpan(ind_row,0,ind_konec-ind_row+1,1)
        self.tableWidget.setSpan(ind_row1,1,ind_konec-ind_row1+1,1)