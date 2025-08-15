import sys
from PyQt6.QtWidgets import QApplication
from ui.main_window import MainWindow
from core.api_manager import APIManager

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # 初始化API管理器
    api_manager = APIManager()

    # 检查是否需要API配置
    if not api_manager.has_valid_api():
        from ui.api_dialog import ApiDialog

        dialog = ApiDialog(api_manager)
        if not dialog.exec():
            sys.exit(0)  # 用户取消配置

    # 启动主窗口
    window = MainWindow(api_manager)
    window.show()

    sys.exit(app.exec())
