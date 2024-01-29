from PyQt5.QtWidgets import QDesktopWidget, QApplication, QWidget, QVBoxLayout, QPushButton, QFileDialog, QTextEdit, QLabel, QComboBox, QSizePolicy, QLineEdit, QMessageBox, QPlainTextEdit
from collections import deque
from PyQt5.QtGui import QIcon
import sys
import os
import shutil
import pickle

class MovetheFile(QWidget):

    def resource_path(self, relative_path):
        try:
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        return os.path.join(base_path, relative_path)
    
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        # 소스 및 타겟 폴더를 위한 변수 초기화
        self.source_folder = ''
        self.target_folder = ''

        # 최근 사용된 폴더 목록
        self.recent_folders = self.load_recent_folders()

        # 아이콘 세팅
        self.setWindowIcon(QIcon(self.resource_path("move_the_file_icon.png")))  

        # 사용자 인터페이스 설정
        vbox = QVBoxLayout()
        self.setLayout(vbox)

        # 소스 폴더 선택 버튼
        self.source_button = QPushButton('Select Source Folder', self)
        self.source_button.clicked.connect(self.select_source)
        self.source_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.source_button)

        # 소스 폴더 경로를 표시하는 텍스트 필드
        self.source_folder_label = QLineEdit(self)
        self.source_folder_label.setReadOnly(True)
        vbox.addWidget(self.source_folder_label)

        # 최근 사용된 소스 폴더를 위한 콤보 박스
        self.source_recent = QComboBox(self)
        self.source_recent.addItem('Recent Folders')
        self.source_recent.addItems(self.recent_folders)
        self.source_recent.currentIndexChanged.connect(self.select_source_recent)
        self.source_recent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.source_recent)

        # 타겟 폴더 선택 버튼
        self.target_button = QPushButton('Select Target Folder', self)
        self.target_button.clicked.connect(self.select_target)
        self.target_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.target_button)

        # 타겟 폴더 경로를 표시하는 텍스트 필드
        self.target_folder_label = QLineEdit(self)
        self.target_folder_label.setReadOnly(True)
        vbox.addWidget(self.target_folder_label)

        # 최근 사용된 타겟 폴더를 위한 콤보 박스
        self.target_recent = QComboBox(self)
        self.target_recent.addItem('Recent Folders')
        self.target_recent.addItems(self.recent_folders)
        self.target_recent.currentIndexChanged.connect(self.select_target_recent)
        self.target_recent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.target_recent)

        # 키워드 입력을 위한 텍스트 필드
        self.keyword_label = QLabel('Keywords (separated by newline):', self)
        vbox.addWidget(self.keyword_label)

        self.keyword_entry = QTextEdit(self)
        self.keyword_entry.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.keyword_entry)

        # 파일 이동 또는 복사를 선택하기 위한 콤보 박스
        self.operation = QComboBox(self)
        self.operation.addItem('Move Files')
        self.operation.addItem('Copy Files')
        self.operation.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        vbox.addWidget(self.operation)

        # 파일 처리 시작 버튼
        self.process_button = QPushButton('Process Files', self)
        self.process_button.clicked.connect(self.process_files)
        self.process_button.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Expanding)
        self.styleProcessButton(self.process_button)  # 스타일 적용
        vbox.addWidget(self.process_button)

        # 처리된 파일 목록을 표시하는 텍스트 필드
        self.log_label = QLabel('Processed Files:', self)
        vbox.addWidget(self.log_label)

        self.log = QPlainTextEdit(self)
        self.log.setReadOnly(True)
        vbox.addWidget(self.log)

        # 윈도우 타이틀 및 크기 설정, 윈도우 표시
        self.setWindowTitle('File Moving Program')
        self.setGeometry(300, 300, 800, 600)
        self.centerWindow()

        self.show()

    def centerWindow(self):
        # 창을 화면의 중앙에 배치하는 메소드
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def load_recent_folders(self):
        # 최근 사용된 폴더 목록을 불러옴
        try:
            with open('recent_folders.pickle', 'rb') as f:
                return pickle.load(f)
        except FileNotFoundError:
            return deque(maxlen=5)

    def save_recent_folders(self):
        # 최근 사용된 폴더 목록을 저장
        with open('recent_folders.pickle', 'wb') as f:
            pickle.dump(self.recent_folders, f)

    def add_recent_folder(self, folder):
        # 폴더를 최근 사용된 폴더 목록에 추가
        if folder in self.recent_folders:
            self.recent_folders.remove(folder)
        self.recent_folders.appendleft(folder)
        self.save_recent_folders()

    def select_source(self):
        # 소스 폴더 선택
        self.source_folder = QFileDialog.getExistingDirectory(self, 'Select Source Folder')
        if self.source_folder:
            self.source_folder_label.setText(self.source_folder)
            self.add_recent_folder(self.source_folder)
            self.source_recent.clear()
            self.source_recent.addItem('Recent Folders')
            self.source_recent.addItems(self.recent_folders)

    def select_source_recent(self, index):
        # 최근 사용된 소스 폴더 선택
        if index > 0:
            self.source_folder = self.recent_folders[index-1]
            self.source_folder_label.setText(self.source_folder)

    def select_target(self):
        # 타겟 폴더 선택
        self.target_folder = QFileDialog.getExistingDirectory(self, 'Select Target Folder')
        if self.target_folder:
            self.target_folder_label.setText(self.target_folder)
            self.add_recent_folder(self.target_folder)
            self.target_recent.clear()
            self.target_recent.addItem('Recent Folders')
            self.target_recent.addItems(self.recent_folders)

    def select_target_recent(self, index):
        # 최근 사용된 타겟 폴더 선택
        if index > 0:
            self.target_folder = self.recent_folders[index-1]
            self.target_folder_label.setText(self.target_folder)

    def process_files(self):
        # 파일 처리
        try:
            keywords = self.keyword_entry.toPlainText().split('\n')
            # 키워드가 입력되지 않은 경우 함수 종료
            if not any(keywords):
                QMessageBox.information(self, "알림", "키워드를 입력해주세요.")
                return
            processed_files = []
            for file_name in os.listdir(self.source_folder):
                if any(keyword in file_name for keyword in keywords if keyword):
                    source_file = os.path.join(self.source_folder, file_name)
                    target_file = os.path.join(self.target_folder, file_name)
                    # 파일 이동 또는 복사
                    if self.operation.currentText() == 'Move Files':
                        shutil.move(source_file, target_file)
                    else:
                        shutil.copy2(source_file, target_file)
                    processed_files.append(file_name)
            if processed_files:
                # 처리된 파일 목록 표시
                self.log.appendPlainText(f"\n{len(processed_files)} 파일이 {self.operation.currentText()}되었습니다:\n" + "\n\n".join(processed_files))
                QMessageBox.information(self, "성공", f"{len(processed_files)} 파일 처리가 완료되었습니다.")
            else:
                QMessageBox.information(self, "알림", "키워드와 일치하는 파일이 없습니다.")
        except Exception as e:
            QMessageBox.critical(self, "오류", str(e))

    def styleProcessButton(self, button):
        # 프로세스 버튼 스타일링
        button.setStyleSheet("""
            QPushButton {
                background-color: #007AFF; color: white;
                border-radius: 5px; padding: 10px; font-size: 18px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
        """)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = MovetheFile()
    sys.exit(app.exec_())
