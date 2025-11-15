import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout,QLCDNumber, QHBoxLayout, QMainWindow

class mainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Basic Qt App Example")
        self.setGeometry(100, 100, 280, 80)
        
        container = QWidget()
        self.setCentralWidget(container)
        
        # Create a vertical layout manager to arrange widgets within the window.
        mainLay = QHBoxLayout()
        #layout2 = QVBoxLayout()
       # layout3 = QVBoxLayout()
        col1 = QVBoxLayout()
        col2 = QVBoxLayout()
        
    
       
        # Create a button widget.
        button = QPushButton("Hello world!")
        #lcd = QLCDNumber()
        # Add the button to the layout.
        col1.addWidget(button)
        col2.addWidget(QPushButton("Button 2"))

        #layout.addWidget(lcd)

        # Set the layout for the main window.
        mainLay.addLayout( col1 )
        mainLay.addLayout( col2 )
        container.setLayout(mainLay)


def main():
    # Create the application object. Exactly one is needed for every Qt application.
    app = QApplication(sys.argv)

    # Create an instance of the main window.
    window = mainWin()

    # Show the window on the screen.
    window.show()

    # Start the application's event loop and wait for user input.
    app.exec()

if __name__ == "__main__":
    main()