"""
将目录下所有的文件转换为指定的编码格式
"""
import os
import codecs
import chardet
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QLineEdit, QPushButton, QFileDialog, QVBoxLayout, QWidget, QHBoxLayout, QComboBox, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt

class TextEncodingConverter(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("文本编码转换工具")
        self.setGeometry(100, 100, 500, 300)

        self.init_ui()

    def init_ui(self):
        main_widget = QWidget()
        main_layout = QVBoxLayout()

        # Directory selection
        directory_layout = QHBoxLayout()
        directory_label = QLabel("目录:")
        self.directory_entry = QLineEdit()
        directory_button = QPushButton("选择")
        directory_button.clicked.connect(self.select_directory)

        # Convert button
        convert_button = QPushButton("转换")
        convert_button.clicked.connect(self.convert_directory)

        directory_layout.addWidget(directory_label)
        directory_layout.addWidget(self.directory_entry)
        directory_layout.addWidget(directory_button)
        directory_layout.addWidget(convert_button)

        # File type selection
        file_type_layout = QHBoxLayout()
        file_type_label = QLabel("文件类型:")
        self.file_type_combo = QComboBox()
        self.file_type_combo.addItems(["------", "txt", "py", "csv"])
        file_type_layout.addWidget(file_type_label)
        file_type_layout.addWidget(self.file_type_combo)

        encoding_label = QLabel("编码格式:")
        self.encoding_combo = QComboBox()
        self.encoding_combo.addItems(["utf-8", "utf-16", "gbk"])
        file_type_layout.addWidget(encoding_label)
        file_type_layout.addWidget(self.encoding_combo)

        # Log
        log_label = QLabel("输出:")
        self.log_text = QTextEdit()
        self.log_text.setReadOnly(True)

        # Progress bar
        self.progress_bar = QProgressBar()

        main_layout.addLayout(directory_layout)
        main_layout.addLayout(file_type_layout)
        main_layout.addWidget(log_label)
        main_layout.addWidget(self.log_text)
        main_layout.addWidget(self.progress_bar)

        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self, "选择目录")
        if directory:
            self.directory_entry.setText(directory)

    def convert_directory(self):
        directory_path = self.directory_entry.text()
        if not directory_path:
            self.log("请先选择目录.")
            return

        file_type_filter = self.file_type_combo.currentText()
        if file_type_filter.startswith("------"):
            file_type_filter = "*.*"
        else:
            file_type_filter = file_type_filter.split(" ")[0]

        to_encoding = self.encoding_combo.currentText()
        files_to_convert = self.get_files_to_convert(directory_path, file_type_filter)

        self.progress_bar.setRange(0, len(files_to_convert))
        self.progress_bar.setValue(0)

        for file_path in files_to_convert:
            self.convert_encoding(file_path, to_encoding)
            self.progress_bar.setValue(self.progress_bar.value() + 1)

    def get_files_to_convert(self, directory_path, file_type_filter):
        files_to_convert = []
        for root, dirs, files in os.walk(directory_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                if file_path.endswith(file_type_filter) or file_type_filter == '*.*':
                    files_to_convert.append(file_path)
        return files_to_convert

    def convert_encoding(self, file_path, to_encoding='utf-8'):
        try:
            with open(file_path, 'rb') as file:
                content = file.read()
                from_encoding = self.detect_encoding(content)
            with codecs.open(file_path, 'r', encoding=from_encoding) as file:
                content = file.read()
            with codecs.open(file_path, 'w', encoding=to_encoding) as file:
                file.write(content)
            self.log(f"转换完成: {file_path} 原始编码 {from_encoding}")
        except Exception as e:
            self.log(f"转换异常 {file_path}: {e}")

    def detect_encoding(self, content):
        result = chardet.detect(content)
        return result['encoding']

    def log(self, message):
        self.log_text.append(message)

if __name__ == "__main__":
    app = QApplication([])
    converter = TextEncodingConverter()
    converter.show()
    app.exec_()
