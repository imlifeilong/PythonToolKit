import os
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit, QPushButton, QFileDialog, QTextEdit, QProgressBar
from PyQt5.QtCore import Qt


class FileRenamer(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 创建布局
        main_layout = QVBoxLayout()

        # 选择文件目录和确定按钮部分
        dir_layout = QHBoxLayout()
        self.dir_label = QLabel("选择文件目录:")
        self.dir_line_edit = QLineEdit()
        self.dir_button = QPushButton("选择目录")
        self.dir_button.clicked.connect(self.select_directory)
        self.confirm_button = QPushButton("确定")
        self.confirm_button.clicked.connect(self.rename_files)
        dir_layout.addWidget(self.dir_label)
        dir_layout.addWidget(self.dir_line_edit)
        dir_layout.addWidget(self.dir_button)
        dir_layout.addWidget(self.confirm_button)
        main_layout.addLayout(dir_layout)

        # 输入源字符串部分
        source_layout = QHBoxLayout()
        self.source_label = QLabel("源文件名中的字符串:")
        self.source_line_edit = QLineEdit()
        source_layout.addWidget(self.source_label)
        source_layout.addWidget(self.source_line_edit)
        main_layout.addLayout(source_layout)

        # 输入替换字符串部分
        replace_layout = QHBoxLayout()
        self.replace_label = QLabel("替换的字符串:")
        self.replace_line_edit = QLineEdit()
        replace_layout.addWidget(self.replace_label)
        replace_layout.addWidget(self.replace_line_edit)
        main_layout.addLayout(replace_layout)

        # 进度条
        self.progress_bar = QProgressBar(self)
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        main_layout.addWidget(self.progress_bar)

        # 日志显示区
        self.log_text_edit = QTextEdit()
        self.log_text_edit.setReadOnly(True)
        main_layout.addWidget(self.log_text_edit)

        # 设置布局
        self.setLayout(main_layout)
        self.setWindowTitle('批量修改文件名')
        self.show()

    def select_directory(self):
        # 打开文件目录选择对话框
        directory = QFileDialog.getExistingDirectory(self, "选择文件目录")
        if directory:
            self.dir_line_edit.setText(directory)

    def rename_files(self):
        # 获取用户输入的目录、源字符串和替换字符串
        directory = self.dir_line_edit.text()
        source_str = self.source_line_edit.text()
        replace_str = self.replace_line_edit.text()

        if not directory or not os.path.isdir(directory):
            return

        # 清空日志显示区
        self.log_text_edit.clear()
        self.progress_bar.setValue(0)

        # 获取所有需要处理的文件列表
        files_to_process = [filename for filename in os.listdir(directory) if source_str in filename]
        total_files = len(files_to_process)

        for index, filename in enumerate(files_to_process):
            # 构建新的文件名
            new_filename = filename.replace(source_str, replace_str)
            old_file_path = os.path.join(directory, filename)
            new_file_path = os.path.join(directory, new_filename)
            try:
                # 重命名文件
                os.rename(old_file_path, new_file_path)
                # 在日志显示区添加替换成功的记录
                log_message = f"成功将 {filename} 替换为 {new_filename}"
                self.log_text_edit.append(log_message)
            except Exception as e:
                print(f"重命名 {filename} 时出错: {e}")

            # 更新进度条
            progress = int((index + 1) / total_files * 100)
            self.progress_bar.setValue(progress)
            QApplication.processEvents()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    renamer = FileRenamer()
    sys.exit(app.exec_())