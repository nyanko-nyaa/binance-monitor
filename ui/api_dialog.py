from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QCheckBox, QMessageBox
)


class ApiDialog(QDialog):
    def __init__(self, api_manager, parent=None):
        super().__init__(parent)
        self.api_manager = api_manager
        self.setWindowTitle("API密钥配置")
        self.setModal(True)

        layout = QVBoxLayout()

        # API Key 输入
        api_key_layout = QHBoxLayout()
        api_key_layout.addWidget(QLabel("API Key:"))
        self.api_key_edit = QLineEdit()
        api_key_layout.addWidget(self.api_key_edit)
        layout.addLayout(api_key_layout)

        # API Secret 输入
        api_secret_layout = QHBoxLayout()
        api_secret_layout.addWidget(QLabel("API Secret:"))
        self.api_secret_edit = QLineEdit()
        self.api_secret_edit.setEchoMode(QLineEdit.EchoMode.Password)
        api_secret_layout.addWidget(self.api_secret_edit)
        layout.addLayout(api_secret_layout)

        # 记住密钥选项
        self.remember_check = QCheckBox("记住我的API密钥")
        self.remember_check.setChecked(True)
        layout.addWidget(self.remember_check)

        # 按钮
        button_layout = QHBoxLayout()
        confirm_btn = QPushButton("确认")
        confirm_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(confirm_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def accept(self):
        api_key = self.api_key_edit.text().strip()
        api_secret = self.api_secret_edit.text().strip()

        if not api_key or not api_secret:
            QMessageBox.warning(self, "警告", "API Key和Secret不能为空")
            return

        try:
            self.api_manager.set_api(
                api_key,
                api_secret,
                self.remember_check.isChecked()
            )
            super().accept()
        except Exception as e:
            QMessageBox.critical(self, "错误", f"保存API密钥时出错: {str(e)}")