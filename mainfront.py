import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton, QMenuBar, QStatusBar, QMainWindow
from PyQt6.QtCore import QRect, QSize, Qt, QCoreApplication,QThread, pyqtSignal, QTime
from PyQt6.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve
import time
import threading
from PyQt6.QtGui import QPixmap, QColor

imgFileBase = "static/images/"

openTalk = "faceOpen.png"
smileClosed = "faceSmile.png"
sad = "sad.png"
superHappy = "superHappy.png"
supersad = "superSad.png"
surprised = "surprise.png"
angry = "faceAngry.png"


class MockHardwareAPI:
    def toggle_lights(self):
        return True  # Always "turn on" lights (mocking the API)

class FlashingLightsWorker(QThread):
    # Signal to communicate with the main thread (UI)
    update_signal = pyqtSignal(str)

    def __init__(self, hardware_api):
        super().__init__()
        #self.hardware_api = hardware_api
        self.hardware_api = MockHardwareAPI()
        #self.setup_external_control() #commented to avoid crash
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


# Function to apply animation when the button is hovered over
        def animate_button_hover():
            # On hover, scale the button up a little bit
            self.animation.setStartValue(self.pushButton.geometry())
            self.animation.setEndValue(QRect(self.pushButton.x() - 5, self.pushButton.y() - 5, self.pushButton.width() + 10, self.pushButton.height() + 10))
            self.animation.start()

        # Function to revert the animation when the mouse leaves
        def animate_button_leave():
            # On mouse leave, scale the button back to normal size
            self.animation.setStartValue(self.pushButton.geometry())
            self.animation.setEndValue(QRect(self.pushButton.x() + 5, self.pushButton.y() + 5, self.pushButton.width() - 10, self.pushButton.height() - 10))
            self.animation.start()

        # Connect hover events to trigger animations
        self.pushButton.setGraphicsEffect(None)
        self.pushButton.installEventFilter(self)

        # When the mouse enters the button's area
        def eventFilter(self, obj, event):
            if obj == self.pushButton:
                if event.type() == QtCore.QEvent.Type.Enter:
                    animate_button_hover()
                elif event.type() == QtCore.QEvent.Type.Leave:
                    animate_button_leave()
            return super().eventFilter(obj, event)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1464, 1146)
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0)")
        # Central Widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(40, 40, 300, 300))  # Set the geometry for placement and size
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align the image
        self.image_label.setObjectName("image_label")
        
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(40, 40, 300, 300))

        # Line 2 (Vertical Line Divider)
        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(870, 0, 31, 1101))
        self.line_2.setStyleSheet("color: rgb(255,255,255)")
        self.line_2.setLineWidth(10)
        self.line_2.setMidLineWidth(10)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        # Label above Chat Input
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(290, 940, 171, 51))  # Adjust position as needed
        self.label.setStyleSheet("color: rgb(160, 255, 166); font-size: 20px")
        self.label.setObjectName("label")

        # Chatbot Input (Text Entry Box)
        self.chatbotEnter = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.chatbotEnter.setGeometry(QtCore.QRect(40, 1040, 631, 29))  # Adjust position as needed
        self.chatbotEnter.setStyleSheet("background-color: rgb(200,200,200)")
        self.chatbotEnter.setObjectName("chatbotEnter")
        self.chatbotEnter.editingFinished.connect(self.enterPress)

        # Fixed Chat Text Box (Read-only, Multi-line)
        self.chattext_box = QtWidgets.QTextEdit(parent=self.centralwidget)
        #self.chattext_box.setGeometry(QtCore.QRect(40, 390, 811, 531))  # Adjust position and size
        self.chattext_box.setPlaceholderText("This is a fixed text box (user can't edit).")
        self.chattext_box.setReadOnly(True)  # Make it read-only so the user can't modify the text
        #self.chattext_box.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        self.chattext_box.setObjectName("chattext_box")
        self.chattext_box.setGeometry(QtCore.QRect(30, 390, 811, 531))  # Adjust position as needed
        self.chattext_box.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        #self.plainTextEdit.setObjectName("plainTextEdit")


        # Set fixed size for the text box to make it non-resizable
        self.chattext_box.setFixedSize(811, 531)  # Width = 811px, Height = 531px

        
        
        # Push Button 1 (Action Button) with animations
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(1040, 30, 261, 41))  # Adjust position as needed
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("""
            QPushButton {
                color: rgb(160, 255, 166); 
                border: 2px solid rgb(160, 255, 166);
                border-radius: 5px; 
                padding: 5px 10px;
                background-color: rgb(30, 30, 30);  # Dark background to start
            }
            QPushButton:hover {
                background-color: rgb(60, 60, 60);  # Lighter background on hover
                border-color: rgb(255, 255, 255);  # Border color changes to white on hover
                color: rgb(255, 255, 255);  # Text color changes to white
            }
            QPushButton:pressed {
                background-color: rgb(50, 50, 50);  # Darker background on press
                border-color: rgb(100, 255, 100);  # Border color changes to green on press
                color: rgb(100, 255, 100);  # Text color changes to green on press
            }
        """)
        self.pushButton.setObjectName("pushButton")

        # Create a QPropertyAnimation for scaling effect
        self.animation = QPropertyAnimation(self.pushButton, b"geometry")
        self.animation.setDuration(200)  # Duration of animation (in milliseconds)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)  # Smooth animation curve

        

        # Push Button 2 (Another Action Button)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(1040, 130, 261, 41))  # Adjust position as needed
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

        """  def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SPEAK TO ME:"))
        self.pushButton.setText(_translate("MainWindow", "Initiate Strategic Illumination"))
        self.pushButton_2.setText(_translate("MainWindow", "Initiate Radio Control"))
"""

    def retranslateUi(self, MainWindow):
        _translate = QCoreApplication.translate
        #Main.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SPEAK TO ME"))

        self.pushButton.setText(_translate("MainWindow", "Initiate Strategic Illumination"))
        self.pushButton_2.setText(_translate("MainWindow", "Initiate Radio Control"))

        """Setup the main window and layout."""
        #self.setWindowTitle("Image Animation Example")
        
        """
        # Create central widget and layout
        self.centralwidget = QWidget(MainWindow)
        #self.layout = QVBoxLayout(self.centralwidget)

        self.image_label = QLabel(MainWindow)
        self.layout.addWidget(self.image_label)
        self.setup_animation()"""
        


    #external GPIO control setup
    def setup_external_control(self):
        """Set up the external worker (background loop)"""
        self.hardware_api = ExternalHardwareAPI()#will crash it for now
        self.worker = FlashingLightsWorker(self.hardware_api)
        self.worker.update_signal.connect(self.update_ui_from_worker)
    
    def update_ui_from_worker(self, status_text):
        """Update the UI with the flashing light status."""
        self.status_label.setText(status_text)

    #self.worker.start() #start
    #self.worker.stop() #stop


    def chatresponse(self, entered_text):
        response = f"Echo: {entered_text}"
        return response

    def external_update_text(self, new_text):
        """Simulate an external function that updates the text box."""
        # Here, you can set the text of the text box from an external source
        new_text = "Updated text from an external function."#update before implementation
        self.chattext_box.setText(new_text)


    def enterPress(self):        
        """Handle the event when the user presses Enter in the chatbot input field."""
        # Get the text from the chatbot input field
        entered_text = self.chatbotEnter.text()
        print(f"User entered: {entered_text}")
        
        # Clear the input field after getting the text
        self.chatbotEnter.clear()

        # Generate a response from the entered text (you could call a different function here)
        response = self.chatresponse(entered_text)
        
        # Set the response text into the chattext_box
        self.chattext_box.setText(response)
   
    



    
        
        
        
    def setup_animation(self):
        # QLabel to display images
        
        #self.setCentralWidget(self.centralwidget)
        """Setup the image animation functionality."""
         # List of image paths for the animation
        self.talkimagePaths = [
            smileClosed,
            openTalk,
            smileClosed,
            openTalk,
            smileClosed,
            # Add more images as needed
        ]
        
        self.current_frame = 0  # To track the current image frame
        
        # Create a QTimer to update the image
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # Update every 100 milliseconds

    def update_image(self):
        """Update the image on the QLabel."""
        try:
            pixmap = QPixmap(self.talkimagePaths[self.current_frame])
            if not pixmap.isNull():  # Check if the image was loaded successfully
                self.image_label.setPixmap(pixmap)
            else:
                print(f"Failed to load image: {self.talkimagePaths[self.current_frame]}")
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Update to the next image
        self.current_frame += 1
        if self.current_frame >= len(self.talkimagePaths):
            self.current_frame = 0  # Loop back to the first image
def main():
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    #MainWindow.setWindowTitle("Chatbot Interface")
    #window = Ui_MainWindow()
    MainWindow.setGeometry(100, 100, 600, 400)
    MainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()