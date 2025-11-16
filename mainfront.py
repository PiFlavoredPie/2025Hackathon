import sys
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QMenuBar, QStatusBar, QMainWindow
from PyQt6.QtCore import QRect, QSize, Qt, QCoreApplication,QThread, pyqtSignal, QTimer,QPushButton, QLineEdit
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


class mainWin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setObjectName("MainWindow")
        self.resize(1464, 1146)
        self.setStyleSheet("background-color: rgb(0, 0, 0)")

        # Central Widget
        self.centralwidget = QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")

        # Line 2
        self.line_2 = QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QRect(710, 0, 31, 1101))
        self.line_2.setStyleSheet("color: rgb(255,255,255)")
        self.line_2.setLineWidth(10)
        self.line_2.setMidLineWidth(10)
        self.line_2.setFrameShape(QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        # Chatbot Input
        self.chatbotEnter = QLineEdit(parent=self.centralwidget)
        self.chatbotEnter.setGeometry(QRect(40, 1040, 631, 29))
        self.chatbotEnter.setStyleSheet("background-color: rgb(200,200,200)")
        self.chatbotEnter.setObjectName("chatbotEnter")
        self.chatbotEnter.editingFinished.connect(self.enterPress,"chatbotEnter")
        
        # Label
        self.label = QLabel(parent=self.centralwidget)
        self.label.setGeometry(QRect(290, 940, 171, 51))
        self.label.setStyleSheet("color: rgb(160, 255, 166); font-size: 20px")
        self.label.setObjectName("label")

        # Set up menu bar and status bar
        self.menubar = QMenuBar(parent=self)
        self.menubar.setGeometry(QRect(0, 0, 1464, 30))
        self.setMenuBar(self.menubar)

        self.statusbar = QStatusBar(parent=self)
        self.setStatusBar(self.statusbar)
        #self.setup_animation()
        
        # Create a QLineEdit (fixed text box)
        self.chattext_box = QLineEdit(self)
        self.chattext_box.setPlaceholderText("This is a fixed text box (user can't edit).")
        self.chattext_box.setReadOnly(True)  # Make it read-only so the user can't modify the text
        self.mainLay.addWidget(self.chattext_box)
        
        # Layout (example: QVBoxLayout for centralwidget)
        self.mainLay = QVBoxLayout(self.centralwidget)
        self.centralwidget.setLayout(self.mainLay)
    
        self.setCentralWidget(self.centralwidget)
        
        # Retranslate UI
        self.retranslateUi()


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


    def chatresponse(entered_text):
        response = f"Echo: {entered_text}"
        return response

    def external_update_text(self, new_text):
        """Simulate an external function that updates the text box."""
        # Here, you can set the text of the text box from an external source
        new_text = "Updated text from an external function."#update before implementation
        self.chattext_box.setText(new_text)


    def enterPress(self):
        Stype = self.sender().objectName()
        entered_text = self.chatbotEnter.text()
        print(f"User entered: {entered_text}")
        
        self.chatbotEnter.clear()
        if(Stype == "chatbotEnter"):
            return chatresponse(entered_text)
        else:
            return ""

   
    



    def retranslateUi(self):
        _translate = QCoreApplication.translate
        self.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label.setText(_translate("MainWindow", "SPEAK TO ME"))

        self.setup_window()
        self.setup_animation()
        
    def setup_window(self):
        """Setup the main window and layout."""
        self.setWindowTitle("Image Animation Example")
        self.setGeometry(100, 100, 600, 400)
        
        # Create central widget and layout
        self.centralwidget = QWidget(self)
        self.layout = QVBoxLayout(self.centralwidget)
        
        
        
    def setup_animation(self):
        # QLabel to display images
        self.image_label = QLabel(self)
        self.layout.addWidget(self.image_label)
        self.setCentralWidget(self.centralwidget)
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
        # Load the current image
        pixmap = QPixmap(self.talkimagePaths[self.current_frame])
        self.image_label.setPixmap(pixmap)
        
        # Update to the next image
        self.current_frame += 1
        if self.current_frame >= len(self.talkimagePaths):
            self.current_frame = 0  # Loop back to the first image

def main():
    app = QApplication([])

    window = mainWin()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()