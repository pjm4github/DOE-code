import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt5.QtCore import pyqtSlot

class Window(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle('GridLAB-D Simulation')
        self.setGeometry(50, 50, 200, 200)  # x, y, width, height

        # Central widget
        self.centralWidget = QWidget()
        self.setCentralWidget(self.centralWidget)

        # Layout
        self.layout = QVBoxLayout()
        self.centralWidget.setLayout(self.layout)

        # Quit Button
        self.quitButton = QPushButton('Quit')
        self.quitButton.clicked.connect(self.on_quit_clicked)
        self.layout.addWidget(self.quitButton)

        # Label for displaying messages
        self.messageLabel = QLabel('')
        self.layout.addWidget(self.messageLabel)

        # Display initial message
        self.xoutput("Beginning simulation...")

    @pyqtSlot()
    def on_quit_clicked(self):
        self.xoutput("Simulation done.")
        self.close()

    def xoutput(self, message):
        # Method to update the message label
        self.messageLabel.setText(message)
        self.messageLabel.adjustSize()  # Adjust the size to fit the text

def xstart():
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    xstart()