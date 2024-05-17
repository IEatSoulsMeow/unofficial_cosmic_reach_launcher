import os
import subprocess
import sys
import configparser
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class CosmicReachLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unofficial Cosmic Reach Launcher")
        self.setWindowIcon(QIcon('assets/ucrl_icon.png'))
        self.setMinimumSize(400, 200)
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.init_ui()
        self.check_and_update_text_file()

    def init_ui(self):
        # Create a QLineEdit to display the first line from config.txt
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Config file path")

        # Create a QPushButton
        selectLoc = QPushButton("Select Location")
        openGame = QPushButton("Open Game")
        updateButton = QPushButton("Update")
        selectLoc.clicked.connect(self.select_location)
        openGame.clicked.connect(self.run_file)
        updateButton.clicked.connect(self.update_config_file)

        # Create layouts
        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(selectLoc)
        buttonLayout.addWidget(openGame)

        updateLayout = QHBoxLayout()
        updateLayout.addWidget(updateButton)

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.text_input)
        mainLayout.addLayout(updateLayout)
        mainLayout.addLayout(buttonLayout)

        # Set the main layout
        self.setLayout(mainLayout)
    
    def check_and_update_text_file(self):
        if 'Path' not in self.config['DEFAULT']:
            default_text = "C:\\Users\\User\\AppData\\Roaming\\itch\\apps\\cosmic-reach\\Cosmic Reach.exe"
            self.config['DEFAULT']['Path'] = default_text
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
        
        self.update_text_input()

    def update_text_input(self):
        if 'Path' in self.config['DEFAULT']:
            first_line = self.config['DEFAULT']['Path']
            self.text_input.setText(first_line)

    def run_file(self):
        if 'Path' in self.config['DEFAULT']:
            file_path = self.config['DEFAULT']['Path']
            if file_path:
                file_ext = os.path.splitext(file_path)[1].lower()

                if file_ext == ".py":
                    subprocess.run(["python", file_path])
                elif file_ext == ".exe":
                    subprocess.run([file_path])
                elif file_ext == ".java":
                    subprocess.run(["javac", file_path])
                    java_file_name = os.path.splitext(os.path.basename(file_path))[0]
                    subprocess.run(["java", java_file_name])
                else:
                    print("Unsupported file type")
            else:
                print("No file path specified in config.ini")
        else:
            print("No 'Path' key found in config.ini")

    def select_location(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Game Location", "", "Executable Files (*.exe);;All Files (*)", options=options)
        if file_path:
            print("Selected file:", file_path)
            self.config['DEFAULT']['Path'] = file_path
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            self.text_input.setText(file_path)
    
    def update_config_file(self):
        new_file_path = self.text_input.text()
        if new_file_path:
            self.config['DEFAULT']['Path'] = new_file_path
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = CosmicReachLauncher()
    launcher.show()
    sys.exit(app.exec_())
