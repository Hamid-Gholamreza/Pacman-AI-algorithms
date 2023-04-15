import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.Qt import *
import random
import time
import enum
from queue import PriorityQueue
from PyQt5.QtGui import QColor, QPalette
from PyQt5.QtGui import QPixmap, QIcon



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
        self.list_of_blocks = []
        self.list_of_foods = []
        self.pacman = []

       
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

        self.pacman_position = None

        self.objectLabel = QLabel("Object:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.objectLabel, 0, 0)

        self.objectCombobox = QComboBox()
        self.objectCombobox.addItems(['Pacman', 'Food', 'Block'])
        self.objectCombobox.setFixedSize(150, 30)
        self.objectCombobox.setEnabled(False)
        self.objectCombobox.activated.connect(self.object_choosing)
        self.form.addWidget(self.objectCombobox, 0, 1)

        self.density = QLabel("Density:")
        self.objectLabel.setFixedSize(150, 50)
        self.form.addWidget(self.density, 0, 2)

        self.densityCombobox = QComboBox()
        self.densityCombobox.addItems(['4', '3', '2', '1'])
        self.densityCombobox.setFixedSize(150, 30)
        self.form.addWidget(self.densityCombobox, 0, 3)

        self.clearButton = QPushButton('Clear')
        self.clearButton.setFixedSize(80, 30)
        self.clearButton.clicked.connect(self.clear_button)
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

        self.generateRandomPatternButton = QPushButton('Generate Random Pattern')
        self.generateRandomPatternButton.setFixedSize(180, 30)
        self.form.addWidget(self.generateRandomPatternButton, 2, 3)
        self.generateRandomPatternButton.clicked.connect(self.generate_random_pattern_button)

        self.searchButton  = QPushButton('Search')
        self.searchButton.setFixedSize(80, 30)
        # self.searchButton.clicked.connect(self.search_button)
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


        self.pacmanFlag = False


        self.CreateButtons()
        self.vertical.addLayout(self.form)
        Widget.setLayout(self.vertical)
        self.setCentralWidget(Widget)

    
    def CreateButtons(self):
        for row in range(self.rows):
            for column in range(self.columns):
                if (row == 0 or row == 19) or (column == 0 or column == 29):
                    button = PushButton('', style=self.Styles["Black"], row=row, column=column, color="black")
                    button.setObjectName(f"{row}-{column}")
                    self.layout.addWidget(button, row + 1, column)
                else:
                    button = PushButton('', style=self.Styles["White"], row=row, column=column, color="white")
                    button.setObjectName(f"{row}-{column}")
                    self.Buttons[row][column] = button
                    button.setEnabled(False)
                    self.layout.addWidget(button, row+1, column)
                    self.ButtonGroup.addButton(button)
                    button.clicked.connect(self.object_choosing)


    def click_change_color(self, index):
        if index == 0:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(False)
            self.objectCombobox.setEnabled(False)
        elif index == 1:
            for button in self.ButtonGroup.buttons():
                button.setEnabled(True)
            self.objectCombobox.setEnabled(True)


    def click_for_block(self):
        sender = self.sender()
        sender.setProperty('text', '')
        if sender.palette().color(sender.backgroundRole()) == QColor('white'):
            sender.setStyleSheet("background-color: black;"
                                "border :0.5px solid gray;")
            self.list_of_blocks.append(sender)

        elif sender.palette().color(sender.backgroundRole()) == QColor('black'):
            sender.setStyleSheet("background-color: white;"
                                "border :0.5px solid gray;")
            self.list_of_blocks.remove(sender)


    def clear_button(self):
        for button in self.ButtonGroup.buttons():
            button.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;")
            button.setText('')
            button.setIcon(QIcon())
        self.list_of_blocks = []
        self.list_of_foods = []
        self.pacman = []
        self.pacmanFlag = False


    def object_choosing(self):
        sender = self.sender()
        if self.objectCombobox.currentIndex() == 0:     ### for pacman
            self.click_for_pacman()

        elif self.objectCombobox.currentIndex() == 1:    ### for food
            self.click_for_food()

        elif self.objectCombobox.currentIndex() == 2:  ### for object
            self.click_for_block()


    def click_for_food(self):
        sender = self.sender()
        if sender.text() == '':
            font = QFont('Arial', 20)
            sender.setProperty('text', '•')
            sender.setFont(font)
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")
            self.list_of_foods.append(sender)

        elif sender.text() == '•':
            sender.setProperty('text', '')
            sender.setStyleSheet("background-color: white;"
                                 "border :0.5px solid gray;"
                                 "color: orange")
            self.list_of_foods.remove(sender)


    def click_for_pacman(self):
        sender = self.sender()
        pixmap = QPixmap('./images/pacman_icon.png')
        if not self.pacmanFlag:
            pixmap = pixmap.scaled(sender.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
            icon = QIcon(pixmap)
            sender.setIcon(icon)
            self.pacmanFlag = True
            self.pacman.append(sender)
        else:
            sender.setIcon(QIcon())
            self.pacmanFlag = False
            self.pacman.remove(sender)



    def generate_random_pattern_button(self):
        self.clear_button()
        list_of_blocks = []
        self.density = self.densityCombobox.currentIndex() + 1               ##### generate random blocks
        for i in range(0, 19):
            block_number_per_row = int(random.randint(0, 28)/ self.density)
            while len(list_of_blocks) < block_number_per_row:
                random_number = random.randint(1, 28)
                if random_number not in list_of_blocks:
                    list_of_blocks.append(random_number)
                    self.list_of_blocks.append(f"{i}-{random_number}")
            list_of_blocks = []

        for block_id in self.list_of_blocks:
            button = self.findChild(PushButton, block_id)
            button.setStyleSheet("background-color: black;"
                                "border :0.5px solid gray;")





        for i in range(0, random.randint(1, 504 - (len(self.list_of_blocks) + 1))):
            food_button = self.findChild(PushButton, f"{random.randint(1, 18)}-{random.randint(1, 28)}")
            if food_button.palette().color(food_button.backgroundRole()).name() != 'black':
                food_button.setProperty('text', '•')
                font = QFont('Arial', 20)
                food_button.setFont(font)
                food_button.setStyleSheet("background-color: white;"
                                     "border :0.5px solid gray;"
                                     "color: orange")



        while self.pacmanFlag == False:
            pacman_button = self.findChild(PushButton, f"{random.randint(1, 18)}-{random.randint(1, 28)}")         #### generate random pacman
            self.pacman = [pacman_button.objectName()]
            if pacman_button.palette().color(pacman_button.backgroundRole()).name() != 'black' and pacman_button.text() != '•':
                pacman_button.setStyleSheet("background-color: white;"
                                     "border :0.5px solid gray;")
                pixmap = QPixmap('./images/pacman_icon.png')
                pixmap = pixmap.scaled(pacman_button.size(), aspectRatioMode=Qt.KeepAspectRatio, transformMode=Qt.SmoothTransformation)
                icon = QIcon(pixmap)
                self.pacmanFlag = True
                pacman_button.setIcon(icon)
                for button in self.ButtonGroup.buttons():
                    button.setEnabled(True)







app = QApplication(sys.argv)
w = MyWindow()
w.setWindowTitle('Searchs Algorithm')
w.show()
sys.exit(app.exec_())