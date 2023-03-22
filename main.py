import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import random
import time
import enum
from queue import PriorityQueue







class PushButton(QPushButton):
    def __init__(self, text, style,row,column, color, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setStyleSheet(style)
        self.setText(text)
        self.setMinimumSize(QSize(35, 35))
        self.setMaximumSize(QSize(35, 35))
        self.color=color
        






class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        self.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)
        width=1000
        height=700
        self.setFixedSize(width,height)


        self.rows = 20
        self.columns = 30
        self.Buttons = [[0 for _ in range(self.columns)] for __ in range(self.rows)]
       
        self.Styles = {
            "White": """
                background-color:white;
                max-height:35px;
                max-width:35px;
                border :0.5px solid gray;
                """,
            "Black": """
                background-color:black;
                max-height:35px;
                max-width:35px;
                border :0.5px solid gray;
                """,
            }
        



        Widget= QWidget()
        self.vertical = QVBoxLayout()
        self.inWidget = QWidget()
        self.layout = QGridLayout(self.inWidget)
        self.vertical.addWidget(self.inWidget)
        self.CreateButtons()
        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)



    
    def CreateButtons(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row==0 or row==19) or(column==0 or column==29) :
                    button = PushButton('', style=self.Styles["Black"],row=row,column=column, color="black")
                    self.layout.addWidget(button,row + 1, column)
                else:
                    button = PushButton('', style=self.Styles["White"],row=row,column=column, color="white")
                    self.Buttons[row][column]=button
                    button.setEnabled(False)
                    self.layout.addWidget(button,row+1,column)

    




app = QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()
sys.exit(app.exec_())