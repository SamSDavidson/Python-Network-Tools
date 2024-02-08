import os, sys, subprocess
from PyQt6 import QtGui, QtCore, QtWidgets
from PyQt6.QtCore import Qt
from qt_material import apply_stylesheet

# TO DO: Add help window support, Add switches for calls


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
        self.side_layout = QtWidgets.QVBoxLayout()
        central_widget = QtWidgets.QWidget()
        self.setCentralWidget(central_widget)
        central_widget.setLayout(main_layout)
        self.setWindowTitle("Network Tools")
        self.flag_box = QtWidgets.QHBoxLayout()
        self.output_section = QtWidgets.QVBoxLayout()

        # Create Widgets
        label = QtWidgets.QLabel("Network Tools")
        self.os_select = QtWidgets.QComboBox()
        self.command_select = QtWidgets.QComboBox()
        self.argument_field = QtWidgets.QLineEdit()
        self.run_button = QtWidgets.QPushButton("Run")
        self.help_button = QtWidgets.QPushButton("Help")
        self.output_window = QtWidgets.QPlainTextEdit()

        # Set Connections
        self.os_select.currentIndexChanged.connect(self.on_os_select)
        self.command_select.currentTextChanged.connect(self.on_command_select)
        self.run_button.clicked.connect(self.on_run_button)
        self.help_button.clicked.connect(self.on_help_button)

        # Add Widgets to Layout
        main_layout.addWidget(label)
        self.side_layout.addWidget(self.os_select)
        self.side_layout.addWidget(self.command_select)
        self.side_layout.addLayout(self.flag_box)
        self.side_layout.addWidget(self.argument_field)
        self.side_layout.addWidget(self.run_button)
        self.side_layout.addWidget(self.help_button)
        self.output_section.addWidget(self.output_window)

        # Add Layouts
        self.side_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.side_layout.addStretch()
        main_layout.addLayout(self.side_layout)
        main_layout.addLayout(self.output_section)

        # Set Default Fields
        self.os_select.addItems(["Windows", "Linux"])
        self.os_commands = self.windows_commands
        self.command_select.addItems(self.os_commands)

    def on_os_select(self, index):
        self.command_select.clear()
        if index == 0:
            self.current_os = "Windows"
            self.reset_index(self.windows_commands)
        elif index == 1:
            self.current_os = "Linux"
            self.reset_index(self.linux_commands)

    def reset_index(self, clist):
        if self.command_select.currentIndex() == 0:
            self.command_select.addItems(clist)
        else:
            self.command_select.addItems(clist)
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

    # Append flags to horizontal layout box
    def create_flags(self, flags):
        for flag in flags:
            self.flag_box.addWidget(QtWidgets.QCheckBox(flag))

    # Run commands based on argument field
    # TO DO - import selected flags into run command
    def on_run_button(self):
        self.run_command(
            [f"{self.command_select.currentText()}", f"{self.argument_field.text()}"]
        )

    def on_help_button(self):
        self.run_command(["man", f"{self.command_select.currentText()}"])
        # f'{self.argument_field.text()}

    def run_command(self, commands):
        try:
            output, error = subprocess.Popen(
                commands,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            ).communicate()
            if error.decode() == "":
                self.output_window.setPlainText(output.decode())
            else:
                self.output_window.setPlainText(error.decode())
        except OSError as e:
            self.output_window.setPlainText(f"Execution Failed: {e}")


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    apply_stylesheet(app, theme="light_blue.xml")
    window.show()
    sys.exit(app.exec())
