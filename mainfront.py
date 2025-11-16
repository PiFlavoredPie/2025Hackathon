import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton, QMenuBar, QStatusBar, QMainWindow
from PyQt6.QtCore import QRect, QSize, Qt, QCoreApplication, QThread, pyqtSignal, QTime
from PyQt6.QtCore import QTimer
import time
import threading
from PyQt6.QtGui import QPixmap

imgFileBase = "static/images/"

openTalk = "faceOpen.png"
smileClosed = "faceSmile.png"
sad = "sad.png"
superHappy = "superHappy.png"
supersad = "superSad.png"
surprised = "surprise.png"
angry = "faceAngry.png"


class FlashingLightsWorker(QThread):
    # Signal to communicate with the main thread (UI)
    update_signal = pyqtSignal(str)

    def __init__(self, hardware_api):
        super().__init__()
        self.hardware_api = hardware_api
        self.running = True  # Control flag for the loop

    def run(self):
        """The loop that controls the lights on an external system (hardware or API)."""
        while self.running:
            self.toggle_lights()
            time.sleep(1)  # Flash every second (adjust as needed)

    def stop(self):
        """Stop the background task."""
        self.running = False

    def toggle_lights(self):
        """Toggle the lights and update the UI with the new state."""
        state = self.hardware_api.toggle_lights()
        state_text = "Lights ON" if state else "Lights OFF"
        self.update_signal.emit(state_text)


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1464, 1146)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0)")

        # Central Widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        # Line 2 (Vertical Line Divider)
        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(710, 0, 31, 1101))
        self.line_2.setStyleSheet("color: rgb(255,255,255)")
        self.line_2.setLineWidth(10)
        self.line_2.setMidLineWidth(10)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        # Label above Chat Input
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(290, 940, 171, 51))
        self.label.setStyleSheet("color: rgb(160, 255, 166); font-size: 20px")
        self.label.setObjectName("label")

        # Chatbot Input (Text Entry Box)
        self.chatbotEnter = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.chatbotEnter.setGeometry(QtCore.QRect(40, 1040, 631, 29))
        self.chatbotEnter.setStyleSheet("background-color: rgb(200,200,200)")
        self.chatbotEnter.setObjectName("chatbotEnter")
        self.chatbotEnter.editingFinished.connect(self.enterPress)

        # Fixed Chat Text Box (Read-only)
        self.chattext_box = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.chattext_box.setGeometry(QtCore.QRect(40, 390, 811, 531))
        self.chattext_box.setPlaceholderText("This is a fixed text box (user can't edit).")
        self.chattext_box.setReadOnly(True)
        self.chattext_box.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        self.chattext_box.setObjectName("chattext_box")

        # Plain Text Edit (User Editable Area)
        self.plainTextEdit = QtWidgets.QPlainTextEdit(parent=self.centralwidget)
        self.plainTextEdit.setGeometry(QtCore.QRect(30, 390, 811, 531))
        self.plainTextEdit.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        self.plainTextEdit.setObjectName("plainTextEdit")

        # Push Button 1 (Action Button)
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1040, 30, 261, 41))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);"
                                      "border-radius: 5px; padding: 5px 10px;")
        self.pushButton.setObjectName("pushButton")

        # Push Button 2 (Another Action Button)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1040, 130, 261, 41))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);"
                                        "border-radius: 5px; padding: 5px 10px;")
        self.pushButton_2.setObjectName("pushButton_2")

        # Menu Bar Setup
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1464, 30))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Status Bar Setup
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Finalizing Setup
        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def setup_window(self, MainWindow):
        """Setup the main window and layout."""
        #self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        self.centralwidget = QWidget(MainWindow)
        self.layout = QVBoxLayout(self.centralwidget)
        MainWindow.setCentralWidget(self.centralwidget)

    def enterPress(self):
        Stype = self.sender().objectName()
        entered_text = self.chatbotEnter.text()
        print(f"User entered: {entered_text}")
        self.chatbotEnter.clear()
        if(Stype == "chatbotEnter"):
            return chatresponse(entered_text)
        else:
            return ""

    def setup_animation(self, MainWindow):
        """Setup the image animation functionality."""
        self.talkimagePaths = [
            smileClosed,
            openTalk,
            smileClosed,
            openTalk,
            smileClosed,
        ]
        
        self.current_frame = 0
        
        # Create a QTimer to update the image
        self.timer = QTimer(MainWindow)  # Set MainWindow as the parent
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # Update every 100 milliseconds


    def update_image(self):
        """Update the image on the QLabel."""
        pixmap = QPixmap(self.talkimagePaths[self.current_frame])
        self.image_label.setPixmap(pixmap)
        
        # Update to the next image
        self.current_frame += 1
        if self.current_frame >= len(self.talkimagePaths):
            self.current_frame = 0

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        self.label.setText(_translate("MainWindow", "SPEAK TO ME"))
        self.setup_window(MainWindow)
        self.image_label = QLabel(self.centralwidget)
        self.layout.addWidget(self.image_label)
        self.setup_animation(MainWindow)


def main():
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
