import sys
import subprocess
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QLineEdit, QPushButton, QGridLayout,
    QMessageBox, QFileDialog, QHBoxLayout, QVBoxLayout, QFrame
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt

class NANDFlashInterfaceGUI(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("NAND_FLASH_INTERFACE")
        self.setMinimumWidth(600)

        # Style: blue-green gradient theme
        self.setStyleSheet("""
            QWidget {
                background: qlineargradient(
                    x1:0, y1:0, x2:1, y2:1,
                    stop:0 #009999, stop:1 #006666
                );
                font-family: 'Segoe UI';
                font-size: 14px;
                color: #ffffff;
            }
            QLabel {
                font-weight: bold;
                color: #ffffff;
            }
            QLineEdit {
                padding: 6px;
                border: 1px solid #ffffff;
                border-radius: 6px;
                background-color: #e0f7fa;
                color: #003333;
            }
            QPushButton {
                padding: 6px 15px;
                background-color: #004d4d;
                color: white;
                border-radius: 8px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #008080;
            }
        """)

        outer_layout = QVBoxLayout()

        # Title label
        title = QLabel("NAND_FLASH_INTERFACE")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Segoe UI", 18, QFont.Bold))
        outer_layout.addWidget(title)

        # Divider
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        outer_layout.addWidget(line)

        layout = QGridLayout()

        # Friendly labels → CLI flags
        self.field_map = {
            "Memory Block Number:": ("-b", "Block index in flash memory."),
            "Memory Page Number:": ("-p", "Page index within the block."),
            "Memory Plane Index:": ("-s", "Plane number to read/write."),
            "Column Address (in bytes):": ("-a", "Byte offset within the page."),
            "Size of Buffer (in bytes):": ("-S", "Size of data to read/write."),
            "Chip Selection (Enter 0 or 1):": ("-c", "Choose chip 0 or 1."),
        }

        self.fields = {}
        row = 0
        for label_text, (flag, tooltip) in self.field_map.items():
            input_field = QLineEdit()
            input_field.setToolTip(tooltip)
            self.fields[flag] = input_field

            layout.addWidget(QLabel(label_text), row, 0)
            layout.addWidget(input_field, row, 1)
            row += 1

        # File selection
        file_label = QLabel("Input File to Process:")
        self.file_input = QLineEdit()
        self.file_input.setToolTip("Select the input file that needs to be processed.")
        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse_file)

        file_layout = QHBoxLayout()
        file_layout.addWidget(self.file_input)
        file_layout.addWidget(browse_button)

        layout.addWidget(file_label, row, 0)
        layout.addLayout(file_layout, row, 1)
        row += 1

        # Run + Help buttons
        self.run_button = QPushButton("Run Executable")
        self.run_button.clicked.connect(self.run_command)

        self.help_button = QPushButton("Help")
        self.help_button.clicked.connect(self.show_help)

        button_layout = QHBoxLayout()
        button_layout.addWidget(self.run_button)
        button_layout.addWidget(self.help_button)

        layout.addLayout(button_layout, row, 0, 1, 2, alignment=Qt.AlignCenter)

        outer_layout.addLayout(layout)
        self.setLayout(outer_layout)

    def browse_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Select File")
        if file_name:
            self.file_input.setText(file_name)

    def run_command(self):
        exe_name = "demo.exe"
        cmd = [exe_name]

        for flag, input_field in self.fields.items():
            value = input_field.text().strip()
            if value:
                cmd.extend([flag, value])

        file_path = self.file_input.text().strip()
        if file_path:
            cmd.extend(["-f", file_path])

        try:
            subprocess.run(cmd, check=True)
            QMessageBox.information(self, "Success", f"{exe_name} ran successfully.")
        except FileNotFoundError:
            QMessageBox.critical(self, "Error", f"{exe_name} not found.")
        except subprocess.CalledProcessError:
            QMessageBox.critical(self, "Error", f"{exe_name} execution failed.")

    def show_help(self):
        help_text = """
Help - Field Descriptions

1. Memory Block Number:
   The flash memory block to read/write from.

2. Memory Page Number:
   A sub-section within the selected block.

3. Memory Plane Index:
   Flash memory may have multiple planes — choose the index.

4. Column Address (in bytes):
   The byte offset where data starts in the page.

5. Size of Buffer (in bytes):
   Total number of bytes to read or write.

6. Chip Selection (0 or 1):
   Select chip 0 or chip 1 depending on hardware.

7. Input File to Process:
   Choose the data or command file to be processed.
        """
        QMessageBox.information(self, "Help", help_text.strip())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = NANDFlashInterfaceGUI()
    window.show()
    sys.exit(app.exec_())
