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
        self.load_theme()  # Load the theme based on saved configuration after initializing UI
        self.check_and_update_text_file()

    def init_ui(self):
        # Create QTabWidget
        tabs = QTabWidget()

        # Create tabs
        home_tab = QWidget()
        settings_tab = QWidget()
        
        # Initialize edit_button
        self.edit_mode = False
        self.edit_button = QPushButton("Edit Instance")
        self.edit_button.clicked.connect(self.toggle_edit_mode)

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
        title_settings_info_version = QLabel("U.C.R.L 0.0.4")
        title_settings_info_contact = QLabel("By IEatSoulsMeow - contact@darkmodecats.com")
        title_settings_info_link = QLabel("github.com/IEatSoulsMeow/unnoficial_cosmic_reach_launcher") 
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

        # Create a scroll area for the home tab
        home_scroll_area = QScrollArea()
        home_scroll_area.setWidgetResizable(True)

        # Create a container widget for home layout
        home_container = QWidget()
        self.home_layout = QVBoxLayout()  # Change to instance variable to add buttons later

        self.add_instance_buttons()

        # Add "Add Instance" button at the bottom
        add_instance_button = QPushButton("Add Instance")
        add_instance_button.clicked.connect(self.add_instance)
        self.home_layout.addWidget(add_instance_button)
        
        # Add "Edit Instance" button below "Add Instance" button
        self.home_layout.addWidget(self.edit_button)

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
                
    def update_instance_button_text_and_path(self, old_name, new_name):  # Updated method to update button text and path
        for i in range(self.home_layout.count()):
            widget = self.home_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text().strip() == old_name:
                widget.setText("  " + new_name)
                widget.clicked.disconnect()  # Disconnect previous connections
                widget.clicked.connect(lambda _, n=new_name: self.handle_instance_button(n))
                break
    
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
                self.visualmodeDropDown.setCurrentIndex(0)
            elif theme_mode == "Light":
                QApplication.instance().setStyleSheet("")
                self.visualmodeDropDown.setCurrentIndex(1)
            elif theme_mode == "Auto":
                if darkdetect.theme() == "Dark":
                    QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
                else:
                    QApplication.instance().setStyleSheet("")
                self.visualmodeDropDown.setCurrentIndex(2)
        else:
            # Theme mode is not specified, default to "Auto"
            if darkdetect.theme() == "Dark":
                QApplication.instance().setStyleSheet(qdarktheme.load_stylesheet())
                self.visualmodeDropDown.setCurrentIndex(2)
            else:
                QApplication.instance().setStyleSheet("")
                self.visualmodeDropDown.setCurrentIndex(1)
            
            # Save the default theme mode to config.ini
            self.config['DEFAULT']['ThemeMode'] = "Auto"
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
    
    def load_instance_buttons(self):
        if 'Instances' not in self.config.sections():
            self.config.add_section('Instances')

    def add_instance_buttons(self):
        if 'Instances' in self.config:
            for instance in self.config['Instances']:
                # Exclude 'Path' and 'ThemeMode' keys
                if instance.lower() not in ['path', 'thememode']:
                    instance_button = QPushButton("  " + instance)  # Add space for icon
                    instance_button.clicked.connect(lambda _, name=instance: self.handle_instance_button(name))
                    instance_button.setIcon(QIcon("assets/ucrl_icon.png"))  # Add icon
                    self.home_layout.addWidget(instance_button)
    
    def handle_instance_button(self, name):  # Updated method to handle instance button click
        path = self.config['Instances'].get(name, None)
        if path:
            if self.edit_mode:
                self.edit_instance(name, path)
            else:
                self.run_instance(path)
    
    def toggle_edit_mode(self):
        self.edit_mode = not self.edit_mode
        if hasattr(self, 'edit_button'):
            if self.edit_mode:
                self.edit_button.setText("Cancel Edit")
            else:
                self.edit_button.setText("Edit Instance")
        else:
            print("Edit button does not exist.")

    
    def edit_instance(self, name, path):
        dialog = QDialog(self)
        dialog.setWindowTitle("Edit Instance")

        name_label = QLabel("Name:")
        path_label = QLabel("Path:")
        name_edit = QLineEdit(name)
        path_edit = QLineEdit(path)
        select_location_button = QPushButton("Select Location")
        select_location_button.clicked.connect(lambda: self.select_location_dialog(path_edit))

        save_button = QPushButton("Save")
        save_button.clicked.connect(lambda: self.save_instance_edit(dialog, name, name_edit.text(), path_edit.text()))

        delete_button = QPushButton("Delete")  # New delete button
        delete_button.setStyleSheet("background-color: red; color: white;")
        delete_button.clicked.connect(lambda: self.delete_instance(dialog, name))

        layout = QVBoxLayout()
        layout.addWidget(name_label)
        layout.addWidget(name_edit)
        layout.addWidget(path_label)
        layout.addWidget(path_edit)
        layout.addWidget(select_location_button)
        layout.addWidget(save_button)
        layout.addWidget(delete_button)  # Add the delete button to the layout
        dialog.setLayout(layout)
        dialog.exec_()

    def delete_instance(self, dialog, name):
        reply = QMessageBox.question(self, 'Delete Instance', f"Are you sure you want to delete the instance '{name}'?",
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.config.remove_option('Instances', name)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            
            dialog.accept()
            self.remove_instance_button(name)
            self.update_instance_buttons()
    
    def remove_instance_button(self, name):
        for i in reversed(range(self.home_layout.count())):
            widget = self.home_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text().strip() == name:
                self.home_layout.removeWidget(widget)
                widget.deleteLater()
                break

    def add_instance(self):
        name, ok = QInputDialog.getText(self, 'Add Instance', 'Enter instance name:')
        if ok and name:
            file_path, _ = QFileDialog.getOpenFileName(self, "Select Instance Location", "", "Executable Files (*.exe);;All Files (*)")
            if file_path:
                self.config.set('Instances', name, file_path)
                with open('config.ini', 'w') as configfile:
                    self.config.write(configfile)
                # Instead of updating all buttons, add only the new one
                self.add_single_instance_button(name)
                
    def add_single_instance_button(self, name):
        button = QPushButton("  " + name)
        button.clicked.connect(lambda _, n=name: self.handle_instance_button(n))
        button.setIcon(QIcon("assets/ucrl_icon.png"))
        # Insert the new button before the "Add Instance" and "Edit Instance" buttons
        self.home_layout.insertWidget(self.home_layout.count() - 3, button)

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
            elif file_ext == ".jar":
                subprocess.run(["java", "-jar", path])
            else:
                print("Unsupported file type")
                
    # Add a method to clear and reload instance buttons
    def update_instance_buttons(self):
        # Clear the layout before re-adding widgets
        while self.home_layout.count():
            child = self.home_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        # Re-add instance buttons
        self.add_instance_buttons()

        # Add "Add Instance" button
        add_instance_button = QPushButton("Add Instance")
        add_instance_button.clicked.connect(self.add_instance)
        edit_instance_button = QPushButton("Edit Instance")
        edit_instance_button.clicked.connect(self.toggle_edit_mode)
        self.home_layout.addWidget(add_instance_button)
        self.home_layout.addWidget(edit_instance_button)

        # Add stretch to push buttons to the top
        self.home_layout.addStretch()
    
    def clear_instance_buttons(self):  # New method to clear instance buttons only
        for i in reversed(range(self.home_layout.count())):
            widget = self.home_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget not in [self.edit_button, self.home_layout.itemAt(self.home_layout.count() - 1).widget()]:
                print(f"Removing widget: {widget}")
                widget.deleteLater()
                
    def add_edit_and_add_buttons(self):
        # Add "Add Instance" button
        add_instance_button = QPushButton("Add Instance")
        add_instance_button.clicked.connect(self.add_instance)
        self.home_layout.addWidget(add_instance_button)

        # Ensure the "Edit Instance" button is visible and properly added
        self.home_layout.addWidget(self.edit_button)
        self.edit_button.setVisible(True)
        self.home_layout.addStretch()

    def select_location_for_edit(self, path_input):
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getOpenFileName(self, "Select New Instance Location", "", "Executable Files (*.exe);;All Files (*)", options=options)
        if file_path:
            path_input.setText(file_path)
            
    def select_location_dialog(self, path_edit):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Instance Location", "", "Executable Files (*.exe);;All Files (*)")
        if file_path:
            path_edit.setText(file_path)
        
    def save_instance_edit(self, dialog, old_name, new_name, path):  # Updated function to accept dialog object
        old_path = self.config['Instances'].get(old_name, None)
        if new_name != old_name or path != old_path:  # Check if either name or path is updated
            if new_name != old_name:
                self.config.remove_option('Instances', old_name)
            self.config.set('Instances', new_name, path)
            with open('config.ini', 'w') as configfile:
                self.config.write(configfile)
            
            dialog.accept()
            
            # Update the corresponding button without removing and re-adding all buttons
            self.update_instance_button_text_and_path(old_name, new_name)
            
            # Disable edit mode before updating instance buttons
            self.edit_mode = False
            self.edit_button.setText("Edit Instance")
            
        else:
            print("No changes made")
            dialog.accept()
            
    def update_instance_button_text(self, old_name, new_name):  # New method to update button text
        for i in range(self.home_layout.count()):
            widget = self.home_layout.itemAt(i).widget()
            if isinstance(widget, QPushButton) and widget.text().strip() == old_name:
                widget.setText("  " + new_name)
                break

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle('Fusion')
    launcher = CosmicReachLauncher()
    launcher.show()
    sys.exit(app.exec_())