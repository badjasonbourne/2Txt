import os
from PySide6.QtWidgets import (QApplication, QMainWindow, QVBoxLayout, QPushButton,
                               QWidget, QLabel, QLineEdit, QTextEdit, QFileDialog)
from PySide6.QtCore import Qt, Slot

class FileBrowserApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('File Browser')
        self.setGeometry(300, 300, 600, 300)  # Adjust size and position

        layout = QVBoxLayout()

        self.folder_edit = QTextEdit()
        self.folder_edit.setPlaceholderText("拖拽文件夹到此区域")
        self.folder_edit.setAcceptDrops(False)
        layout.addWidget(self.folder_edit)

        self.setAcceptDrops(True)  # Accept drag/drop events

        self.save_dir_edit = QLineEdit()
        self.save_dir_edit.setPlaceholderText("选择保存目录")
        layout.addWidget(self.save_dir_edit)

        choose_dir_btn = QPushButton("选择保存目录", self)
        choose_dir_btn.clicked.connect(self.choose_save_directory)
        layout.addWidget(choose_dir_btn)

        start_btn = QPushButton('开始解析', self)
        start_btn.clicked.connect(self.start_parsing)
        layout.addWidget(start_btn)

        central_widget = QWidget()
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    @Slot()
    def choose_save_directory(self):
        save_dir = QFileDialog.getExistingDirectory(self, "选择保存目录")
        self.save_dir_edit.setText(save_dir)

    @Slot()
    def start_parsing(self):
        folder_path = self.folder_edit.toPlainText()
        output_path = self.save_dir_edit.text()
        self.parse_files(folder_path, output_path)

    def parse_files(self, folder_path, output_path):
        if not folder_path or not output_path:
            # Alert the user to select both folder and save directory
            return
        output_file_path = os.path.join(output_path, 'output.txt')
        with open(output_file_path, 'w') as output_file:
            for root, dirs, files in os.walk(folder_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    if not self.is_text_file(file_path):
                        continue
                    output_file.write(f'File Name：{file}\n')
                    output_file.write(f'File Path：{file_path}\n')
                    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                        content = f.read(1024)  # Read first 1024 characters
                    output_file.write(f'Content：\n{content}\n\n')

    def is_text_file(self, file_path):
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore'):
                return True
        except:
            return False

    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, e):
        folder_paths = [url.toLocalFile() for url in e.mimeData().urls() if os.path.isdir(url.toLocalFile())]
        self.folder_edit.setText('\n'.join(folder_paths))

if __name__ == '__main__':
    app = QApplication([])
    ex = FileBrowserApp()
    ex.show()
    app.exec()
