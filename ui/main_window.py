from PyQt6.QtWidgets import (
    QMainWindow, QTableWidget, QTableWidgetItem, QHeaderView,
    QToolBar, QStatusBar, QLabel
)
from PyQt6.QtGui import QColor, QBrush, QAction
from PyQt6.QtCore import Qt, QTimer
from core.binance_client import BinanceClient
from ui.export_dialog import ExportDialog
from core.data_fetcher import DataFetcher
from datetime import datetime



class MainWindow(QMainWindow):
    def __init__(self, api_manager):
        super().__init__()
        self.api_manager = api_manager
        self.binance_client = BinanceClient(api_manager)
        self.fetcher = DataFetcher(self.binance_client)
        self.fetcher.data_fetched.connect(self.update_table)
        self.fetcher.error_occurred.connect(self.show_error)

        self.data = None

        self.setWindowTitle("币安持仓监控")
        self.setGeometry(100, 100, 1000, 600)

        toolbar = QToolBar("主工具栏")
        self.addToolBar(toolbar)

        refresh_action = QAction("刷新", self)
        refresh_action.triggered.connect(self.refresh_data)
        toolbar.addAction(refresh_action)

        export_action = QAction("导出", self)
        export_action.triggered.connect(self.export_data)
        toolbar.addAction(export_action)

        api_action = QAction("API设置", self)
        api_action.triggered.connect(self.show_api_dialog)
        toolbar.addAction(api_action)

        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["币种", "持仓量", "当前价格", "总价值 (USDT)", "占比 (%)"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        self.setCentralWidget(self.table)

        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.status_label = QLabel("就绪")
        self.status_bar.addWidget(self.status_label)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.refresh_data)
        self.timer.start(30000)  # 30秒

        self.refresh_data()

    def refresh_data(self):
        self.status_label.setText("正在获取数据...")
        self.fetcher.start()

    def update_table(self, data):
        self.data = data
        self.table.setRowCount(len(data['holdings']))

        for row, item in enumerate(data['holdings']):
            # 处理价格计算（防止除零）
            price = item['value'] / item['amount'] if item['amount'] > 0 else 0

            self.table.setItem(row, 0, QTableWidgetItem(item['asset']))
            self.table.setItem(row, 1, QTableWidgetItem(f"{item['amount']:,.8f}"))
            self.table.setItem(row, 2, QTableWidgetItem(f"{price:,.4f}"))
            self.table.setItem(row, 3, QTableWidgetItem(f"${item['value']:,.2f}"))
            self.table.setItem(row, 4, QTableWidgetItem(f"{item['percentage']:,.2f}%"))

            if item['percentage'] > 50:
                for col in range(5):
                    self.table.item(row, col).setBackground(QBrush(QColor(255, 255, 0, 100)))

        self.status_label.setText(
            f"最后更新: {self.format_timestamp(data['timestamp'])} | 总价值: ${data['total_value']:,.2f}")

    def show_error(self, message):
        self.status_label.setText(f"错误: {message}")

    def export_data(self):
        if not self.data:
            return

        dialog = ExportDialog(self.data, self)
        dialog.exec()

    def show_api_dialog(self):
        from ui.api_dialog import ApiDialog
        dialog = ApiDialog(self.api_manager, self)
        if dialog.exec():
            self.binance_client.connect()
            self.refresh_data()

    def format_timestamp(self, timestamp):
        """格式化时间戳为可读字符串"""
        return datetime.fromtimestamp(timestamp / 1000).strftime('%Y-%m-%d %H:%M:%S')