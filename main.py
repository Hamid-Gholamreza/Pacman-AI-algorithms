import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import random
import time
import enum
from queue import PriorityQueue
from PyQt5.QtGui import QColor, QPalette




class PushButton(QPushButton):
    def __init__(self, text, style, row, column, color, parent=None):
        super(PushButton, self).__init__(text, parent)
        self.setStyleSheet(style)
        self.setText(text)
        self.setMinimumSize(QSize(35, 35))
        self.setMaximumSize(QSize(35, 35))
        self.color = color
        



class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow, self).__init__()
        width=1000
        height=700
        self.setFixedSize(width, height)


        self.rows = 20
        self.columns = 30

        self.Buttons = [[0 for _ in range(self.columns)] for __ in range(self.rows)]
       
        self.Styles = {
            "White": """
                background-color:white;
                max-height:25px;
                max-width:25px;
                border :0.5px solid gray;
                padding-left: 0px;
                padding-right: 0px;
                """,
            "Black": """
                background-color:black;
                max-height:25px;
                max-width:25px;
                border :0.5px solid gray;
                padding-left: 0px;
                padding-right: 0px;
                """,
            }
        



        Widget = QWidget()
        self.vertical = QVBoxLayout()
        self.inWidget = QWidget()
        self.ButtonGroup = QButtonGroup()

        self.layout = QGridLayout(self.inWidget)
        self.vertical.addWidget(self.inWidget)

        self.form = QGridLayout()

        self.objectLabel = QLabel("Object:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.objectLabel, 0, 0)

        self.objectCombobox = QComboBox()
        self.objectCombobox.addItems(['Packman', 'Food', 'Block'])
        self.objectCombobox.setFixedSize(150, 30)
        self.objectCombobox.setEnabled(False)
        self.objectCombobox.activated.connect(self.object_choosing)
        self.form.addWidget(self.objectCombobox, 0, 1)

        self.density = QLabel("Density:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.density, 0, 2)

        self.densityCombobox = QComboBox()
        self.densityCombobox.addItem('4')
        self.densityCombobox.setFixedSize(150, 30)
        self.form.addWidget(self.densityCombobox, 0, 3)

        self.clearButton = QPushButton('Clear')
        self.clearButton.setFixedSize(80, 30)
        self.clearButton.clicked.connect(self.clear_buttons)
        self.form.addWidget(self.clearButton, 0, 4)

        self.algorithmLabel = QLabel('Algorithm:')
        self.algorithmLabel.setFixedSize(150, 30)
        self.form.addWidget(self.algorithmLabel, 1, 0)

        self.algorithmCombobox = QComboBox()
        self.algorithmCombobox.addItems(['DFS', 'BFS'])
        self.algorithmCombobox.setFixedSize(150, 30)
        self.form.addWidget(self.algorithmCombobox, 1, 1)

        self.animationRateLabel = QLabel('Animation Rate:')
        self.animationRateLabel.setFixedSize(150, 30)
        self.form.addWidget(self.animationRateLabel, 1, 2)

        self.animationRateCombobox = QComboBox()
        self.animationRateCombobox.addItem('Without Animation')
        self.animationRateCombobox.setFixedSize(180, 30)
        self.form.addWidget(self.animationRateCombobox, 1, 3)

        self.undoButton = QPushButton('Undo')
        self.undoButton.setFixedSize(80, 30)
        self.form.addWidget(self.undoButton, 1, 4)

        self.handyStatusLabel = QLabel('Handy Status:')
        self.handyStatusLabel.setFixedSize(150, 30)
        self.form.addWidget(self.handyStatusLabel, 2, 0)

        self.handyStatusCombobox = QComboBox()
        self.handyStatusCombobox.addItems(['UnHandy', 'Handy'])
        self.handyStatusCombobox.setFixedSize(180, 30)
        self.handyStatusCombobox.activated.connect(self.click_change_color)
        self.form.addWidget(self.handyStatusCombobox, 2, 1)

        self.generateRandomPatternButton  = QPushButton('Generate Random Pattern')
        self.generateRandomPatternButton.setFixedSize(180, 30)
        self.form.addWidget(self.generateRandomPatternButton, 2, 3)

        self.searchButton  = QPushButton('Search')
        self.searchButton.setFixedSize(80, 30)
        self.form.addWidget(self.searchButton, 2, 4)

        self.timeOfExecutionLabel = QLabel('Time Of Execution:')
        self.timeOfExecutionLabel.setFixedSize(150, 30)
        self.form.addWidget(self.timeOfExecutionLabel, 3, 1)

        self.timeOfExecutionMessageBox = QPlainTextEdit()
        self.timeOfExecutionMessageBox.setFixedSize(150, 30)
        self.timeOfExecutionMessageBox.setEnabled(False)
        self.form.addWidget(self.timeOfExecutionMessageBox, 3, 2)

        self.openedNodeLabel = QLabel('Opened Node:')
        self.openedNodeLabel.setFixedSize(150, 30)
        self.form.addWidget(self.openedNodeLabel, 3, 3)

        self.openedNodeMessageBox = QPlainTextEdit()
        self.openedNodeMessageBox.setFixedSize(150, 30)
        self.openedNodeMessageBox.setEnabled(False)
        self.form.addWidget(self.openedNodeMessageBox, 3, 4)


        self.CreateButtons()
        self.vertical.addLayout(self.form)
        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)

    
    def CreateButtons(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row == 0 or row == 19) or (column == 0 or column == 29):
                    button = PushButton('', style=self.Styles["Black"], row=row, column=column, color="black")
                    self.layout.addWidget(button, row + 1, column)
                else:
                    button = PushButton('', style=self.Styles["White"], row=row, column=column, color="white")
                    self.Buttons[row][column] = button
                    button.setEnabled(False)
                    self.layout.addWidget(button, row+1, column)
                    self.ButtonGroup.addButton(button)


    def click_change_color(self, index):
        if index == 0:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(False)
            self.objectCombobox.setEnabled(False)
        elif index == 1:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(True)
            self.objectCombobox.setEnabled(True)

    def on_button_clicked(self):
        sender = self.sender()
        sender.setProperty('text', '')
        if sender.palette().color(sender.backgroundRole()) == QColor('white'):
            sender.setStyleSheet("background-color: black;"
                                "border :0.5px solid gray;")

        elif sender.palette().color(sender.backgroundRole()) == QColor('black'):
            sender.setStyleSheet("background-color: white;"
                                "border :0.5px solid gray;")

    def clear_buttons(self):
        for button in self.ButtonGroup.buttons():
            button.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;")
            button.setText('')


    def object_choosing(self, index):
        if index == 1:        # food
            for button in self.ButtonGroup.buttons():
                button.clicked.connect(self.click_for_food)
        elif index == 2:        # block
            for button in self.ButtonGroup.buttons():
                button.clicked.connect(self.on_button_clicked)


    def click_for_food(self):
        sender = self.sender()
        if sender.text() == '':
            font = QFont('Arial', 20)
            sender.setProperty('text', '•')
            sender.setFont(font)
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")

        elif sender.text() == '•':
            sender.setProperty('text', '')
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")




app = QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()
sys.exit(app.exec_())