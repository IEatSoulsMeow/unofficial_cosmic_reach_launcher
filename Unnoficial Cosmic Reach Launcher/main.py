import os
import subprocess
import sys
from file_manipulation import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

def replace_line(file_path, line_number, new_line):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
    except FileNotFoundError:
        lines = []

    while len(lines) < line_number:
        lines.append('\n')

    lines[line_number - 1] = new_line + '\n'

    with open(file_path, 'w') as file:
        file.writelines(lines)

    print(f"Line {line_number} replaced successfully.")

class CosmicReachLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unofficial Cosmic Reach Launcher")
        self.setWindowIcon(QIcon('assets/ucrl_icon.png'))
        self.setMinimumSize(400, 200)
        
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
        openGame.clicked.connect(lambda: self.run_file())
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
        file_path = 'config.txt'  # Change to your text file path
        default_text = "C:\\Users\\User\\AppData\\Roaming\\itch\\apps\\cosmic-reach\\Cosmic Reach.exe"
        # Check if the file exists and has content
        try:
            with open(file_path, 'r') as file:
                first_line = file.readline().strip()
                if not first_line:
                    # Set the first line to default text if it's empty
                    try:
                        with open('config.txt', 'r') as file:
                            replace_line("config.txt", 1, default_text)
                    except FileNotFoundError:
                        open('config.txt', 'x')
                        replace_line("config.txt", 1, default_text)
        except FileNotFoundError:
            # Create the file with default text if it doesn't exist
            with open(file_path, 'w') as file:
                file.write(default_text)
            
        # Update the text input with the new file path
        self.update_text_input()

    def update_text_input(self):
        # Read the first line of config.txt
         # Should replace the code below but I need to put the correct input in the last spot so we can replace the first line of the file
        try:
            with open('config.txt', 'r') as file:
                first_line = file.readline().strip("\n")
                self.text_input.setText(first_line)
        except FileNotFoundError:
            print("Config file not found")

    def run_file(self):
    # Read the first line of config.txt
        config_file = "config.txt"
        try:
            with open(config_file, "r") as file:
                file_path = file.readline().strip()
        except FileNotFoundError:
            print("Config file not found")
            return

        # Check if the file path is valid
        if not file_path:
            print("No file path specified in config.txt")
            return

        # Check file extension
        file_ext = os.path.splitext(file_path)[1].lower()

        if file_ext == ".py":
            # Python file
            subprocess.run(["python", file_path])
        elif file_ext == ".exe":
            # Executable file
            subprocess.run([file_path])
        elif file_ext == ".java":
            # Java file
            # Compile Java file
            subprocess.run(["javac", file_path])
            # Run compiled bytecode
            java_file_name = os.path.splitext(os.path.basename(file_path))[0]
            subprocess.run(["java", java_file_name])
        else:
            print("Unsupported file type")
    
    def select_location(self):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Game Location", "", "Executable Files (*.exe);;All Files (*)", options=options)
        if file_path:
            print("Selected file:", file_path)
            # Update the first line in config.txt
            with open('config.txt', "r+") as file:
                lines = file.readlines()
                lines[0] = file_path + '\n'
                file.seek(0)  # Move the cursor to the beginning of the file
                file.writelines(lines)  # Write the modified lines back to the file
                # Update the text input with the new file path
                self.text_input.setText(file_path)
    
    def update_config_file(self):
        new_file_path = self.text_input.text()
        if new_file_path:
            with open('config.txt', "r+") as file:
                lines = file.readlines()
                lines[0] = new_file_path
                file.seek(0)  # Move the cursor to the beginning of the file
                file.writelines(lines)  # Write the modified lines back to the file



if __name__ == '__main__':
    app = QApplication(sys.argv)
    launcher = CosmicReachLauncher()
    launcher.show()
    sys.exit(app.exec_())