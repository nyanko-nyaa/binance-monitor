from PyQt6.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QComboBox, QCheckBox, QFileDialog,
    QProgressBar, QMessageBox
)
from PyQt6.QtCore import Qt
from utils.exporter import export_data
import os


class ExportDialog(QDialog):
    def __init__(self, data, parent=None):
        super().__init__(parent)
        self.data = data
        self.setWindowTitle("导出持仓数据")
        self.setModal(True)

        layout = QVBoxLayout()

        # 导出格式选择
        format_layout = QHBoxLayout()
        format_layout.addWidget(QLabel("导出格式:"))
        self.format_combo = QComboBox()
        self.format_combo.addItems(["CSV", "Excel"])
        format_layout.addWidget(self.format_combo)
        layout.addLayout(format_layout)

        # 导出选项
        self.only_nonzero_check = QCheckBox("仅导出非零持仓")
        self.only_nonzero_check.setChecked(True)
        layout.addWidget(self.only_nonzero_check)

        self.include_calc_check = QCheckBox("包含价值计算")
        self.include_calc_check.setChecked(True)
        layout.addWidget(self.include_calc_check)

        # 进度条
        self.progress_bar = QProgressBar()
        self.progress_bar.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)

        # 按钮
        button_layout = QHBoxLayout()
        export_btn = QPushButton("导出")
        export_btn.clicked.connect(self.start_export)
        cancel_btn = QPushButton("取消")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(export_btn)
        button_layout.addWidget(cancel_btn)
        layout.addLayout(button_layout)

        self.setLayout(layout)

    def start_export(self):
        file_format = self.format_combo.currentText().lower()
        default_name = f"binance_holdings_{self.data['timestamp']}.{file_format}"

        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "保存文件",
            os.path.join(os.path.expanduser("~"), default_name),
            f"{file_format.upper()} 文件 (*.{file_format})"
        )

        if not file_path:
            return

        options = {
            'only_nonzero': self.only_nonzero_check.isChecked(),
            'include_calc': self.include_calc_check.isChecked()
        }

        self.progress_bar.setVisible(True)

        def progress_callback(value):
            self.progress_bar.setValue(value)

        success = export_data(
            self.data,
            file_path,
            file_format,
            options,
            progress_callback
        )

        self.progress_bar.setVisible(False)

        if success:
            QMessageBox.information(self, "成功", "数据导出成功!")
            self.accept()
        else:
            QMessageBox.critical(self, "错误", "导出数据时出错")