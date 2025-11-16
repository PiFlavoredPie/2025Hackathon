import sys
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QLabel, QFrame, QPushButton, QMenuBar, QStatusBar, QMainWindow
from PyQt6.QtCore import QRect, QSize, Qt, QCoreApplication,QThread, pyqtSignal, QTime
from PyQt6.QtCore import QTimer, QPropertyAnimation, QRect, QEasingCurve
import time
import threading
from PyQt6.QtGui import QPixmap, QColor
import backend.input as inputting

imgFileBase = "static//images//"

openTalk = imgFileBase +"faceOpen.png"
smileClosed = imgFileBase + "faceSmile.png"
sad = imgFileBase +"sad.png"
superHappy = imgFileBase + "superHappy.png"
supersad = imgFileBase + "superSad.png"
surprised = imgFileBase + "surprise.png"
angry = imgFileBase + "faceAngry.png"

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
    emo = "Happy"
    emotionsStore = {"Happy":smileClosed, "VeryHappy":superHappy, "Sad":sad, "VerySad":supersad, "Angry":angry, "Surprised":surprised}
    ScreenWidth = 480
    ScreenHeight = 320
    designedScreenWidth = 480
    designedScreenHeight = 320

    def xAd(self, x):
        return int(x * self.ScreenWidth / self.designedScreenWidth)

    def yAd(self,y):
        return int(y * self.ScreenHeight / self.designedScreenHeight)
    def __init__(self):
        self.animation_runs = 0  # Counter to track the number of runs
        self.max_animation_runs = 3  # Maximum number of times the animation will run
    
    def button_2_pressed(self):
        # Add whatever logic you want to run when the button is pressed
        print("Button 2 was pressed!")
        # You can also call other functions here
        self.some_other_function()

    def button_1_pressed(self):
        # Add whatever logic you want to run when the button is pressed
        print("Button 2 was pressed!")
        # You can also call other functions here
        self.some_other_function()

    def some_other_function(self):
        print("Executing another function after button 2 press!")
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(self.xAd(self.ScreenWidth), self.yAd(self.ScreenHeight))
        MainWindow.setStyleSheet("background-color: rgb(0, 0, 0)")
        # Central Widget
        self.centralwidget = QtWidgets.QWidget(parent=MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(self.xAd(40), self.yAd(20), self.xAd(75), self.yAd(75)))  # Set the geometry for placement and size
        self.image_label.setAlignment(QtCore.Qt.AlignmentFlag.AlignCenter)  # Center align the image
        self.image_label.setObjectName("image_label")
        
        self.image_label = QLabel(self.centralwidget)
        self.image_label.setGeometry(QtCore.QRect(self.xAd(40), self.yAd(20), self.xAd(75), self.yAd(75)))

        # Line 2 (Vertical Line Divider)
        self.line_2 = QtWidgets.QFrame(parent=self.centralwidget)
        self.line_2.setGeometry(QtCore.QRect(self.xAd(290), self.yAd(-20), self.xAd(31), self.yAd(1101)))
        self.line_2.setStyleSheet("color: rgb(255,255,255)")
        self.line_2.setLineWidth(10)
        self.line_2.setMidLineWidth(10)
        self.line_2.setFrameShape(QtWidgets.QFrame.Shape.VLine)
        self.line_2.setFrameShadow(QtWidgets.QFrame.Shadow.Sunken)
        self.line_2.setObjectName("line_2")

        # Label above Chat Input
        self.label = QtWidgets.QLabel(parent=self.centralwidget)
        self.label.setGeometry(QtCore.QRect(self.xAd(100), self.yAd(190), self.xAd(150), self.yAd(31)))
        self.label.setStyleSheet("color: rgb(160, 255, 166); font-size: 20px")
        self.label.setObjectName("label")

        # Chatbot Input (Text Entry Box)
        self.chatbotEnter = QtWidgets.QLineEdit(parent=self.centralwidget)
        self.chatbotEnter.setGeometry(QtCore.QRect(self.xAd(10), self.yAd(230), self.xAd(271), self.yAd(29)))
        self.chatbotEnter.setStyleSheet("background-color: rgb(200,200,200)")
        self.chatbotEnter.setObjectName("chatbotEnter")
        self.chatbotEnter.editingFinished.connect(self.enterPress)
        font = QtGui.QFont()
        font.setPointSize(7)
        self.chatbotEnter.setFont(font)

        # Fixed Chat Text Box (Read-only, Multi-line)
        self.chattext_box = QtWidgets.QTextEdit(parent=self.centralwidget)
        #self.chattext_box.setGeometry(QtCore.QRect(40, 500, 811, 531))  # Adjust position and size
        self.chattext_box.setPlaceholderText("This is a fixed text box (user can't edit).")
        self.chattext_box.setReadOnly(True)  # Make it read-only so the user can't modify the text
        #self.chattext_box.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        self.chattext_box.setObjectName("chattext_box")
        self.chattext_box.setGeometry(QtCore.QRect(self.xAd(10), self.yAd(100), self.xAd(281), self.yAd(91)))  # Adjust position as needed
        self.chattext_box.setStyleSheet("color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166);")
        #self.plainTextEdit.setObjectName("plainTextEdit")


        # Set fixed size for the text box to make it non-resizable
        self.chattext_box.setFixedSize(self.xAd(281), self.yAd(91))  # Width = 811px, Height = 531px

        
        
        # Push Button 1 (Action Button) with animations
        self.pushButton = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(self.xAd(320), self.yAd(10), self.xAd(151), self.yAd(61)))
        self.pushButton.setAutoFillBackground(False)
        self.pushButton.setStyleSheet("QPushButton { color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166); border-radius: 5px; padding: 5px 10px; background-color: rgb(30, 30, 30); } QPushButton:hover { background-color: rgb(60, 60, 60); border-color: rgb(255, 255, 255); color: rgb(255, 255, 255); } QPushButton:pressed { background-color: rgb(50, 50, 50); border-color: rgb(100, 255, 100); color: rgb(100, 255, 100); }")
        self.pushButton.setObjectName("pushButton")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton.setFont(font)
        self.pushButton.clicked.connect(self.button_1_pressed)
        # Create a QPropertyAnimation for scaling effect
        self.animation = QPropertyAnimation(self.pushButton, b"geometry")
        self.animation.setDuration(200)  # Duration of animation (in milliseconds)
        self.animation.setEasingCurve(QEasingCurve.Type.OutQuad)  # Smooth animation curve

        

        # Push Button 2 (Another Action Button)
        self.pushButton_2 = QtWidgets.QPushButton(parent=self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(self.xAd(310), self.yAd(90), self.xAd(161), self.yAd(41)))
        self.pushButton_2.setAutoFillBackground(False)
        self.pushButton_2.setStyleSheet("QPushButton { color: rgb(160, 255, 166); border: 2px solid rgb(160, 255, 166); border-radius: 5px; padding: 5px 10px; background-color: rgb(30, 30, 30); } QPushButton:hover { background-color: rgb(60, 60, 60); border-color: rgb(255, 255, 255); color: rgb(255, 255, 255); } QPushButton:pressed { background-color: rgb(50, 50, 50); border-color: rgb(100, 255, 100); color: rgb(100, 255, 100); }")
        self.pushButton_2.setObjectName("pushButton_2")
        font = QtGui.QFont()
        font.setPointSize(10)
        self.pushButton_2.setFont(font)
        self.pushButton_2.clicked.connect(self.button_2_pressed)


        # Menu Bar Setup
        self.menubar = QtWidgets.QMenuBar(parent=MainWindow)
        self.menubar.setGeometry(QtCore.QRect(self.xAd(0), 0, self.xAd(480), self.yAd(30)))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        # Status Bar Setup
        self.statusbar = QtWidgets.QStatusBar(parent=MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        font = QtGui.QFont()
        font.setPointSize(8)
        self.chattext_box.setFont(font)
        

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
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label.setFont(font)

        self.pushButton.setText(_translate("MainWindow", "Initiate Strategic Illumination"))
        self.pushButton_2.setText(_translate("MainWindow", "Initiate distance location"))

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
        response = inputting.user_prompt(entered_text)

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
        textresponse = response[0]
        emot = response[1]
        print(f"Chatbot emotion: {emot}")
        print(f"Chatbot response: {response}")
        
        # Set the response text into the chattext_box
        self.chattext_box.setText(textresponse)
        self.restartAnimation()
        self.emo = emot
   
    



    
        
        
        
    def setup_animation(self, parent):
        # QLabel to display images
        self.talkimagePaths = [
            smileClosed,
            openTalk,
            smileClosed,
            openTalk,
            smileClosed,
            # Add more images as needed
        ]
        
        self.current_frame = 0  # To track the current image frame
        
        # Create a QTimer and pass the parent (MainWindow) here
        self.timer = QTimer(parent)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(100)  # Update every 100 milliseconds

    def update_image(self):
        """Update the image on the QLabel."""
        try:
            pixmap = QPixmap(self.talkimagePaths[self.current_frame])
            
            pixmap = pixmap.scaled(self.xAd(75), self.yAd(75), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
            
            if not pixmap.isNull():  # Check if the image was loaded successfully
                self.image_label.setPixmap(pixmap)
            else:
                print(f"Failed to load image: {self.talkimagePaths[self.current_frame]}")
        except Exception as e:
            print(f"Error loading image: {e}")
        
        # Update to the next image
        self.current_frame += 1

        # If we've completed a full cycle (reached the end of the image array)
        if self.current_frame >= len(self.talkimagePaths):
            self.current_frame = 0  # Loop back to the first image
            self.animation_runs += 1  # Increment animation run after a full cycle

        # Check if the animation has run the desired number of times
        if self.animation_runs >= self.max_animation_runs:
            self.timer.stop()  # Stop the animation
            self.end_animation()  # Call function for the ending state

    def end_animation(self):
        """Function to run after animation finishes."""
        print("Animation completed 3 times. Switching to rest state.")
        # Here, you can set the final image or run any other code for the "rest state"
        # For example, set a final image as the rest state
        emot = self.emo
        print("Detected int emotion:", emot)
        try:
            pixmap = QPixmap(self.emotionsStore[emot])
            print("mapping success")
        except:
            pixmap = QPixmap(smileClosed)  # Default image if emotion not found
            print("mapping error")
        print("detected final emotion:", emot,"with image:", self.emotionsStore[emot])
        pixmap = pixmap.scaled(self.xAd(75), self.yAd(75), QtCore.Qt.AspectRatioMode.KeepAspectRatio)
        
        final_pixmap = QPixmap(pixmap)  # Replace with actual path
        self.image_label.setPixmap(final_pixmap)
        """Reset animation if needed (for example, if you want to restart it)."""
        """Resets the animation so it can be restarted."""
        print("Resetting animation...")

        # Stop the timer (if running)
        if self.timer is not None and self.timer.isActive():
            self.timer.stop()

        # Reset animation variables
        self.animation_runs = 0
        self.current_frame = 0
        

    def restartAnimation(self):
        """Function to restart the animation."""
        print("Restarting animation...")
        self.animation_runs = 0
        self.current_frame = 0
        if self.timer is not None:
            self.timer.start(100)  # Restart the timer to resume animation

    
        

def main():
    app = QApplication([])
    MainWindow = QMainWindow()
    ui = Ui_MainWindow()
    
    ui.setupUi(MainWindow)
    ui.setup_animation(MainWindow)
    #MainWindow.setWindowTitle("Chatbot Interface")
    #window = Ui_MainWindow()
    MainWindow.setGeometry(0, 0, 480, 320)
    MainWindow.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
    