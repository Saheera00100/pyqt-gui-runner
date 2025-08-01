import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout, QMessageBox, QFileDialog, QHBoxLayout
)

class CommandGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Executable Runner GUI")

        layout = QGridLayout()
        self.fields = {}

        # Define labels and flags
        self.flags = {
            '-b (Block)': '-b',
            '-p (Page)': '-p',
            '-s (Plane Select)': '-s',
            '-a (Column Address)': '-a',
            '-S (Buffer Size)': '-S',
            '-c (Chip Select) [0/1]': '-c',
        }

        row = 0
        for label in self.flags:
            self.fields[self.flags[label]] = QLineEdit()
            layout.addWidget(QLabel(label), row, 0)
            layout.addWidget(self.fields[self.flags[label]], row, 1)
            row += 1

        # Special case for -f (File Stream) with Browse
        file_label = QLabel("-f (File Stream Name)")
        self.file_input = QLineEdit()
        self.browse_button = QPushButton("Browse")
        self.browse_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(self.browse_button)

        layout.addWidget(file_label, row, 0)
        layout.addLayout(file_layout, row, 1)
        row += 1

        self.run_button = QPushButton("Run demo.exe")
        self.run_button.clicked.connect(self.run_command)
        layout.addWidget(self.run_button, row, 0, 1, 2)

        self.setLayout(layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def run_command(self):
        exe_name = "demo.exe"  # change if needed
        cmd = [exe_name]

        for flag, input_field in self.fields.items():
            value = input_field.text().strip()
            if value:
                cmd.extend([flag, value])

        # Add file stream field if present
        file_path = self.file_input.text().strip()
        if file_path:
            cmd.extend(["-f", file_path])

        try:
            result = subprocess.run(cmd, check=True)
            QMessageBox.information(self, "Success", f"{exe_name} ran successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"{exe_name} not found.")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"{exe_name} execution failed.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = CommandGUI()
    window.show()
    sys.exit(app.exec_())
