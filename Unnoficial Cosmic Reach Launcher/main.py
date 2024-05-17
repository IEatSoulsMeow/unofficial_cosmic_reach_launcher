import os
import subprocess
import sys
import qdarktheme
import configparser
import darkdetect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtWidgets import QApplication


class CosmicReachLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unofficial Cosmic Reach Launcher")
        self.setWindowIcon(QIcon('assets/ucrl_icon.png'))
        self.setMinimumSize(400, 200)
        self.resize(500, 300)
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')

        self.init_ui()
        self.check_and_update_text_file()

    def init_ui(self):
        # Create QTabWidget
        tabs = QTabWidget()

        # Create tabs
        home_tab = QWidget()
        settings_tab = QWidget()

        # Add tabs to QTabWidget
        tabs.addTab(home_tab, "Home")
        tabs.addTab(settings_tab, "Settings")

        # Create widgets for Settings
        title_settings_location = QLabel("<u>App Location</u>")
        title_settings_location.setStyleSheet("font-size: 16px;")
        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Config file path")
        selectLoc = QPushButton("Select Location")
        updateButton = QPushButton("Update")
        title_settings_theme = QLabel("<u>Theme</u>")
        title_settings_theme.setStyleSheet("font-size: 16px;")
        self.visualmodeDropDown = QComboBox()  # Make it a member variable
        self.visualmodeDropDown.addItem("Dark")  # Add items to the combo box
        self.visualmodeDropDown.addItem("Light")
        self.visualmodeDropDown.addItem("Auto")
        selectLoc.clicked.connect(self.select_location)
        updateButton.clicked.connect(self.update_config_file)

        # Connect the signal of the combo box to a slot function
        self.visualmodeDropDown.currentIndexChanged.connect(self.change_theme)

        # Layout for Settings
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(title_settings_location)
        settings_layout.addWidget(self.text_input)
        settings_layout.addWidget(updateButton)
        settings_layout.addWidget(selectLoc)
        settings_layout.addWidget(title_settings_theme)
        settings_layout.addWidget(self.visualmodeDropDown)  # Add the combo box
        settings_layout.addStretch()

        # Create a container widget for settings layout
        settings_container = QWidget()
        settings_container.setLayout(settings_layout)

        # Create a QScrollArea for settings tab
        scroll_area = QScrollArea()
        scroll_area.setWidget(settings_container)
        scroll_area.setWidgetResizable(True)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Layout for settings tab with scroll area
        settings_tab_layout = QVBoxLayout()
        settings_tab_layout.addWidget(scroll_area)
        settings_tab.setLayout(settings_tab_layout)

        # Create widgets for Home
        label = QLabel("This is home menu")
        openGame = QPushButton("Open Game")
        openGame.clicked.connect(self.run_file)

        # Layout for Home
        home_layout = QVBoxLayout()
        home_layout.addWidget(label)
        home_layout.addWidget(openGame)
        home_tab.setLayout(home_layout)

        # Main layout
        mainLayout = QVBoxLayout()
        mainLayout.addWidget(tabs)
        
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
    
    def change_theme(self, index):
        # Get the selected item text
        selected_item = self.visualmodeDropDown.currentText()

        # Load the appropriate style sheet based on the selected item
        if selected_item == "Dark":
            QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
            self.config['DEFAULT']['ThemeMode'] = "Dark"
        elif selected_item == "Light":
            QApplication.instance().setStyleSheet("")
            self.config['DEFAULT']['ThemeMode'] = "Light"
        elif selected_item == "Auto":
            if darkdetect.theme() == "Dark":
                QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
            else:
                QApplication.instance().setStyleSheet("")
            self.config['DEFAULT']['ThemeMode'] = "Auto"

        # Save the selected theme mode to config.ini
        with open('config.ini', 'w') as configfile:
            self.config.write(configfile)
    
    def load_theme(self):
        # Load the saved theme mode from config.ini
        if 'ThemeMode' in self.config['DEFAULT']:
            theme_mode = self.config['DEFAULT']['ThemeMode']
            if theme_mode == "Dark":
                QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
            elif theme_mode == "Light":
                QApplication.instance().setStyleSheet("")
            elif theme_mode == "Auto":
                if darkdetect.theme() == "Dark":
                    QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
                else:
                    QApplication.instance().setStyleSheet("")
                pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet())
    launcher = CosmicReachLauncher()
    launcher.show()
    sys.exit(app.exec_())