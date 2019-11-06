import sys
from functools import partial
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QGridLayout
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtWidgets import QLineEdit
from PyQt5.QtWidgets import QPushButton
from PyQt5.QtWidgets import QApplication
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtWidgets import QWidget


# expression evaluation
def evaluateExpression(expression):
    try:
        result = str(eval(expression, {}, {}))
    except Exception:
        result = "ERROR"

    return result




# creating the user interface
class UI(QMainWindow):
    
    # setting the text of the display
    def setDisplayText(self, text):
        self.display.setText(text)
        self.display.setFocus()
    # returning the text of the display
    def getDisplayText(self):
        
        return self.display.text()
    # clearing the display
    def clearDisplay(self):
        self.setDisplayText('')

    
    # setting buttons up.
    def button(self):
        # dictonary with key as button text and value as the button itself
        self.buttons = {}
        # setting the layout of buttons
        buttonsLayout = QGridLayout()
        # dictonary with keys as button text and values as co-ordinates of buttons on grid
        buttons = {'7': (0, 0),
                   '8': (0, 1),
                   '9': (0, 2),
                   '/': (0, 3),
                   'C': (0, 4),
                   '4': (1, 0),
                   '5': (1, 1),
                   '6': (1, 2),
                   '*': (1, 3),
                   '(': (1, 4),
                   '1': (2, 0),
                   '2': (2, 1),
                   '3': (2, 2),
                   '-': (2, 3),
                   ')': (2, 4),
                   '0': (3, 0),
                   '00': (3, 1),
                   '.': (3, 2),
                   '+': (3, 3),
                   '=': (3, 4),
                  }
        # iterating over each item  in the buttons dictonary above and adding buttons to the current object's buttons dictonary.
        for bText, pos in buttons.items():
            self.buttons[bText] = QPushButton(bText)
            self.buttons[bText].setStyleSheet("background-color: orange")
            self.buttons[bText].setFixedSize(50, 50)
            buttonsLayout.addWidget(self.buttons[bText], pos[0], pos[1])
        self.layout.addLayout(buttonsLayout)
    
    
    
    
    # setting up the display
    def display(self):
        # adding editable display and configuring it's layout
        self.display = QLineEdit()
        self.display.setFixedHeight(35)
        self.display.setAlignment(Qt.AlignRight)
        self.display.setStyleSheet("background-color: white")
        self.layout.addWidget(self.display)
        
    
    
    
    def __init__(self):
        super().__init__()
        # setting up the main layout
        self.setWindowTitle('Calculator')
        self.setFixedSize(300,300)
        self.centralwidget = QWidget(self)
        self.setCentralWidget(self.centralwidget)
        self.layout = QVBoxLayout()
        self.centralwidget.setLayout(self.layout)
        self.centralwidget.setStyleSheet("background-color:grey")
        self.display()
        self.button()

# controller connects the view to model
class controller:
    
    
    def connectsignals(self):
        for btext,btn in self.view.buttons.items():
            if btext not in ['C','=']:
                btn.clicked.connect(partial(self.buildExpression,btext))
            self.view.buttons['C'].clicked.connect(self.view.clearDisplay)
            self.view.buttons['='].clicked.connect(self.calculateResult)
            self.view.display.returnPressed.connect(self.calculateResult)

    # builds expression
    def buildExpression(self,sub_exp):
        
        expression = self.view.getDisplayText() + sub_exp
        self.view.setDisplayText(expression)
        
    #result calculaton and setting up the display 
    def calculateResult(self):
        result = self.evaluate(self.view.getDisplayText())
        self.view.setDisplayText(result)
    
    
    def __init__(self,view,model):
        self.evaluate = model
        self.view = view
        self.connectsignals()


if __name__ =="__main__":
    
    claculator = QApplication(sys.argv)
    view = UI()
    view.show()
    model = evaluateExpression
    controller(view, model)
    # event loop
    sys.exit(claculator.exec_())