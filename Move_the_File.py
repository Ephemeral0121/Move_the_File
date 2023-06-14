from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QComboBox, QSizePolicy, QLineEdit, QMessageBox, QPlainTextEdit
from collections import deque
import sys
import os
import shutil
import pickle

class MyApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # Initialize variables for source and target folders
        self.source_folder = ''
        self.target_folder = ''

        # List of recently used folders
        self.recent_folders = self.load_recent_folders()

        # User interface setup
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # Button to select source folder
        self.source_button = QPushButton('Select Source Folder', self)
        self.source_button.clicked.connect(self.select_source)
        self.source_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.source_button)

        # Text field to display the path of the source folder
        self.source_folder_label = QLineEdit(self)
        self.source_folder_label.setReadOnly(True)
        vbox.addWidget(self.source_folder_label)

        # Combo box for recently used source folders
        self.source_recent = QComboBox(self)
        self.source_recent.addItem('Recent Folders')
        self.source_recent.addItems(self.recent_folders)
        self.source_recent.currentIndexChanged.connect(self.select_source_recent)
        self.source_recent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.source_recent)

        # Button to select target folder
        self.target_button = QPushButton('Select Target Folder', self)
        self.target_button.clicked.connect(self.select_target)
        self.target_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.target_button)

        # Text field to display the path of the target folder
        self.target_folder_label = QLineEdit(self)
        self.target_folder_label.setReadOnly(True)
        vbox.addWidget(self.target_folder_label)

        # Combo box for recently used target folders
        self.target_recent = QComboBox(self)
        self.target_recent.addItem('Recent Folders')
        self.target_recent.addItems(self.recent_folders)
        self.target_recent.currentIndexChanged.connect(self.select_target_recent)
        self.target_recent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.target_recent)

        # Text field to enter keywords
        self.keyword_label = QLabel('Keywords (separated by newline):', self)
        vbox.addWidget(self.keyword_label)

        self.keyword_entry = QTextEdit(self)
        self.keyword_entry.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.keyword_entry)

        # Combo box to choose whether to move or copy files
        self.operation = QComboBox(self)
        self.operation.addItem('Move Files')
        self.operation.addItem('Copy Files')
        self.operation.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.operation)

        # Button to start file processing
        self.process_button = QPushButton('Process Files', self)
        self.process_button.clicked.connect(self.process_files)
        self.process_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.process_button)

        # Text field to display the list of processed files
        self.log_label = QLabel('Processed Files:', self)
        vbox.addWidget(self.log_label)

        self.log = QPlainTextEdit(self)
        self.log.setReadOnly(True)
        vbox.addWidget(self.log)

        # Set the title and size of the window, and display the window
        self.setWindowTitle('File Moving Program')
        self.setGeometry(300, 300, 500, 400)
        self.show()

    def load_recent_folders(self):
        # Load the list of recently used folders
        try:
            with open('recent_folders.pickle', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return deque(maxlen=5)

    def save_recent_folders(self):
        # Save the list of recently used folders
        with open('recent_folders.pickle', 'wb') as f:
            pickle.dump(self.recent_folders, f)

    def add_recent_folder(self, folder):
        # Add a folder to the list of recently used folders
        if folder in self.recent_folders:
            self.recent_folders.remove(folder)
        self.recent_folders.appendleft(folder)
        self.save_recent_folders()

    def select_source(self):
        # Select the source folder
        self.source_folder = QFileDialog.getExistingDirectory(self, 'Select Source Folder')
        if self.source_folder:
            self.source_folder_label.setText(self.source_folder)
            self.add_recent_folder(self.source_folder)
            self.source_recent.clear()
            self.source_recent.addItem('Recent Folders')
            self.source_recent.addItems(self.recent_folders)

    def select_source_recent(self, index):
        # Select a recently used source folder
        if index > 0:
            self.source_folder = self.recent_folders[index-1]
            self.source_folder_label.setText(self.source_folder)

    def select_target(self):
        # Select the target folder
        self.target_folder = QFileDialog.getExistingDirectory(self, 'Select Target Folder')
        if self.target_folder:
            self.target_folder_label.setText(self.target_folder)
            self.add_recent_folder(self.target_folder)
            self.target_recent.clear()
            self.target_recent.addItem('Recent Folders')
            self.target_recent.addItems(self.recent_folders)

    def select_target_recent(self, index):
        # Select a recently used target folder
        if index > 0:
            self.target_folder = self.recent_folders[index-1]
            self.target_folder_label.setText(self.target_folder)

    def process_files(self):
        # Process the files
        try:
            keywords = self.keyword_entry.toPlainText().split('\n')
            # If no keywords are entered, the function is exited.
            if not any(keywords):
                QMessageBox.information(self, "Notice", "Please enter keywords.")
                return
            processed_files = []
            for file_name in os.listdir(self.source_folder):
                if any(keyword in file_name for keyword in keywords):
                    source_file = os.path.join(self.source_folder, file_name)
                    target_file = os.path.join(self.target_folder, file_name)
                    # Move or copy the file
                    if self.operation.currentText() == 'Move Files':
                        shutil.move(source_file, target_file)
                    else:
                        shutil.copy2(source_file, target_file)
                    processed_files.append(file_name)
            if processed_files:
                # Display the list of processed files
                self.log.appendPlainText(f"\n{len(processed_files)} files have been {self.operation.currentText()}:\n" + "\n\n".join(processed_files))
                QMessageBox.information(self, "Success", f"{len(processed_files)}File(s) processing is complete.")
            else:
                QMessageBox.information(self, "Notice", "No files match the keywords.")
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MyApp()
    sys.exit(app.exec_())