import os
import subprocess
import sys
import qdarktheme
import configparser
import darkdetect
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QFile, QTextStream
from PyQt5.QtWidgets import QApplication, QInputDialog


class CosmicReachLauncher(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Unofficial Cosmic Reach Launcher")
        self.setWindowIcon(QIcon('assets/ucrl_icon.png'))
        self.setMinimumSize(400, 200)
        self.resize(500, 300)
        
        self.config = configparser.ConfigParser()
        self.config.read('config.ini')
        self.load_instance_buttons() 

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
        selectLoc.clicked.connect(self.select_location)
        updateButton = QPushButton("Update")
        updateButton.clicked.connect(self.update_config_file)
        title_settings_theme = QLabel("<u>Theme</u>")
        title_settings_theme.setStyleSheet("font-size: 16px;")
        self.visualmodeDropDown = QComboBox()  # Make it a member variable
        self.visualmodeDropDown.addItem("Dark")  # Add items to the combo box
        self.visualmodeDropDown.addItem("Light")
        self.visualmodeDropDown.addItem("Auto")
        title_settings_info = QLabel("<u>Info</u>")
        title_settings_info.setStyleSheet("font-size: 16px;")
        title_settings_info_version = QLabel("U.C.R.L 0.0.3")
        title_settings_info_contact = QLabel("By IEatSoulsMeow") # - Maybe include contact info in the future
        title_settings_info_link = QLabel("github.com/IEatSoulsMeow/unnoficial_cosmic_reach_launcher") #('<a href="https://github.com/IEatSoulsMeow/unnoficial_cosmic_reach_launcher/commits/main/">github.com/IEatSoulsMeow/unnoficial_cosmic_reach_launcher/commits/main</a>', self) // Will add this when I can figure out how to colour links
        title_settings_info_link.setOpenExternalLinks(True)

        # Connect the signal of the combo box to a slot function
        self.visualmodeDropDown.currentIndexChanged.connect(self.change_theme)

        # Layout for Settings
        settings_layout = QVBoxLayout()
        settings_layout.addWidget(title_settings_location)
        settings_layout.addWidget(self.text_input)
        settings_layout.addWidget(updateButton)
        settings_layout.addWidget(selectLoc)
        settings_layout.addWidget(title_settings_theme)
        settings_layout.addWidget(self.visualmodeDropDown)
        settings_layout.addWidget(title_settings_info)
        settings_layout.addWidget(title_settings_info_version)
        settings_layout.addWidget(title_settings_info_contact)
        settings_layout.addWidget(title_settings_info_link)
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
        
        # Create a scroll area for the home tab
        home_scroll_area = QScrollArea()
        home_scroll_area.setWidgetResizable(True)

        # Create a container widget for home layout
        home_container = QWidget()
        self.home_layout = QVBoxLayout()  # Change to instance variable to add buttons later

        # Add label to the home layout
        self.home_layout.addWidget(label)
        self.add_instance_buttons()  # Add this line to add instance buttons

        # Add "Add Instance" button at the bottom
        add_instance_button = QPushButton("Add Instance")
        add_instance_button.clicked.connect(self.add_instance)
        self.home_layout.addWidget(add_instance_button)

        self.home_layout.addStretch()
        home_container.setLayout(self.home_layout)
        
        # Set the container as the widget for the scroll area
        home_scroll_area.setWidget(home_container)

        # Layout for Home tab with scroll area
        home_tab_layout = QVBoxLayout()
        home_tab_layout.addWidget(home_scroll_area)
        home_tab.setLayout(home_tab_layout)

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
    
    def load_instance_buttons(self):
        if 'Instances' not in self.config.sections():
            self.config.add_section('Instances')

    def add_instance_buttons(self):
        if 'Instances' in self.config.sections():
            for name, path in self.config.items('Instances'):
                if name != 'path' and name != 'thememode':  # Ensure not loading default keys
                    print(name)
                    button = QPushButton("  " + name)
                    button.clicked.connect(lambda _, p=path: self.run_instance(p))
                    button.setIcon(QIcon("assets/ucrl_icon.png"))
                    
                    edit_button = QPushButton("Edit")
                    edit_button.clicked.connect(lambda _, n=name, p=path: self.edit_instance(n, p))
                    
                    h_layout = QHBoxLayout()
                    h_layout.addWidget(button)
                    h_layout.addWidget(edit_button)
                    
                    container = QWidget()
                    container.setLayout(h_layout)
                    self.home_layout.addWidget(container)
    
    def edit_instance(self, name, path):
        edit_dialog = QDialog(self)
        edit_dialog.setWindowTitle("Edit Instance")
        edit_dialog.setWindowModality(Qt.ApplicationModal)
        edit_dialog.setMinimumSize(400, 200)

        layout = QVBoxLayout()

        name_label = QLabel("Instance Name:")
        name_input = QLineEdit()
        name_input.setText(name)
        
        path_label = QLabel("Instance Location:")
        path_input = QLineEdit()
        path_input.setText(path)

        select_loc_button = QPushButton("Select Location")
        select_loc_button.clicked.connect(lambda: self.select_location_for_edit(path_input))

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_instance_edit(name, name_input.text(), path_input.text(), edit_dialog))

        layout.addWidget(name_label)
        layout.addWidget(name_input)
        layout.addWidget(path_label)
        layout.addWidget(path_input)
        layout.addWidget(select_loc_button)
        layout.addWidget(save_button)

        edit_dialog.setLayout(layout)
        edit_dialog.exec_()

    def add_instance(self):
        name, ok = QInputDialog.getText(self, 'Add Instance', 'Enter instance name:')
        if ok and name:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Instance Location", "", "Executable Files (*.exe);;All Files (*)")
            if file_path:
                self.config.set('Instances', name, file_path)
                with open('config.ini', 'w') as configfile:
                    self.config.write(configfile)
                self.update_instance_buttons()

    def run_instance(self, path):
        if path:
            file_ext = os.path.splitext(path)[1].lower()
            if file_ext == ".py":
                subprocess.run(["python", path])
            elif file_ext == ".exe":
                subprocess.run([path])
            elif file_ext == ".java":
                subprocess.run(["javac", path])
                java_file_name = os.path.splitext(os.path.basename(path))[0]
                subprocess.run(["java", java_file_name])
            else:
                print("Unsupported file type")
                
    # Add a method to clear and reload instance buttons
    def update_instance_buttons(self):
        for i in reversed(range(self.home_layout.count())):
            widget = self.home_layout.itemAt(i).widget()
            if widget is not None:
                widget.deleteLater()
        self.add_instance_buttons()
        add_instance_button = QPushButton("Add Instance")
        add_instance_button.clicked.connect(self.add_instance)
        self.home_layout.addWidget(add_instance_button)
        self.home_layout.addStretch()
    
    def select_location_for_edit(self, path_input):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select New Instance Location", "", "Executable Files (*.exe);;All Files (*)", options=options)
        if file_path:
            path_input.setText(file_path)
        
    def save_instance_edit(self, old_name, new_name, new_path, dialog):
        if new_name and new_path:
            self.config.remove_option('Instances', old_name)
            self.config.set('Instances', new_name, new_path)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            self.update_instance_buttons()
            dialog.accept()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    app.setStyleSheet(qdarktheme.load_stylesheet())
    launcher = CosmicReachLauncher()
    launcher.show()
    sys.exit(app.exec_())