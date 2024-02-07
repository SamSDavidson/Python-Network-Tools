import os
import sys
from PyQt6 import QtGui, QtCore, QtWidgets


class MainWindow(QtWidgets.QMainWindow):
    current_os = None
    linux_commands = {
        "arping": ["-w", "-c", "-f", "-I", "-b", "-U", "-A", "-s", "-D"],
        "arp": ["-d", "-s", "-a", "-g"],
        "dig": ["-4", "-6", "-p", "-f", "-x"],
        "ip": ["-a", "-l", "-r", "-n"],
        "mtr": ["-4", "-6", "-c", "-z", "-n", "-b", "-w"],
        "ping": [],
        "ss": [],
        "traceroute": [],
    }
    windows_commands = {
        "arping": ["-w", "-c", "-f", "-I", "-b", "-U", "-A", "-s", "-D"],
        "arp": ["-d", "-s", "-a", "-g"],
        "ifconfig": [],
        "nbstat": [],
        "netsh": [],
        "netstat": [],
        "nslookup": [],
        "pathping": [],
        "ping": [],
        "tracert": [],
    }

    def __init__(self):
        super(MainWindow, self).__init__()

        # Set up Window
        main_layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        self.setWindowTitle("Network Tools")
        self.flag_box = QtWidgets.QHBoxLayout()

        # Create Widgets
        label = QtWidgets.QLabel("Network Tools")
        self.os_select = QtWidgets.QComboBox()
        self.command_select = QtWidgets.QComboBox()
        self.argument_field = QtWidgets.QLineEdit()
        self.run_button = QtWidgets.QPushButton("Run")

        # Set Connections
        self.os_select.currentIndexChanged.connect(self.on_os_select)
        self.command_select.currentTextChanged.connect(self.on_command_select)
        self.run_button.clicked.connect(self.on_run_button)
        # Add Widgets to Layout
        main_layout.addWidget(label)
        main_layout.addWidget(self.os_select)
        main_layout.addWidget(self.command_select)
        main_layout.addLayout(self.flag_box)
        main_layout.addWidget(self.argument_field)
        main_layout.addWidget(self.run_button)

        # Set Default Fields
        self.os_select.addItems(["Windows", "Linux"])
        self.os_commands = self.windows_commands
        self.command_select.addItems(self.os_commands)

    def on_os_select(self, index):
        self.command_select.clear()
        if index == 0:
            self.current_os = "Windows"
            self.command_select.addItems(self.windows_commands)
        elif index == 1:
            self.current_os = "Linux"
            if self.command_select.currentIndex() == 0:
                self.command_select.addItems(self.linux_commands)
            else:
                self.command_select.addItems(self.linux_commands)
                self.command_select.setCurrentIndex(0)

    def on_command_select(self, text):
        # Clear layoutbox
        for i in reversed(range(self.flag_box.count())):
            self.flag_box.itemAt(i).widget().setParent(None)

        # Display flags based on OS
        if self.os_select.currentIndex() == 0:
            if text in self.windows_commands:
                self.create_flags(self.windows_commands[text])
            else:
                print(f"Windows command '{text}' not found.")
        elif self.os_select.currentIndex() == 1:
            if text in self.linux_commands:
                self.create_flags(self.linux_commands[text])
            else:
                print(f"Linux command '{text}' not found.")

    def create_flags(self, flags):
        for flag in flags:
            self.flag_box.addWidget(QtWidgets.QCheckBox(flag))

    def on_run_button(self):
        if self.os_select.currentIndex() == 0:
            if self.command_select.currentText() in self.windows_commands:
                os.system(f"start {self.command_select.currentText()} {self.argument_field.text()}")
            else:
                print(f"Windows command '{self.command_select.currentText()}' not found.")
        elif self.os_select.currentIndex() == 1:
            if self.command_select.currentText() in self.linux_commands:
                os.system(f"{self.command_select.currentText()} {self.argument_field.text()}")
            else:
                print(f"Linux command '{self.command_select.currentText()}' not found.")
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())
