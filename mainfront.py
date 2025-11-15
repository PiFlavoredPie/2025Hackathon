import sys
from PyQt6.QtWidgets import QApplication, QPushButton, QWidget, QVBoxLayout

def main():
    # Create the application object. Exactly one is needed for every Qt application.
    app = QApplication(sys.argv)

    # Create the main window (a QWidget is a basic container).
    window = QWidget()
    window.setWindowTitle("Basic Qt App Example")
    window.setGeometry(100, 100, 280, 80)
    # Create a vertical layout manager to arrange widgets within the window.
    layout = QVBoxLayout()

    # Create a button widget.
    button = QPushButton("Hello world!")

    # Add the button to the layout.
    layout.addWidget(button)

    # Set the layout for the main window.
    window.setLayout(layout)

    # Show the window on the screen.
    window.show()

    # Start the application's event loop and wait for user input.
    sys.exit(app.exec())

if __name__ == "__main__":
    main()