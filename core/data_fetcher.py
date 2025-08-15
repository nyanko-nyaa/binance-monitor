from PyQt6.QtCore import QThread, pyqtSignal


class DataFetcher(QThread):
    data_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, binance_client):
        super().__init__()
        self.binance_client = binance_client
        self.running = True

    def run(self):
        if not self.binance_client.connect():
            self.error_occurred.emit("无法连接到币安API")
            return

        data = self.binance_client.get_holdings()
        if data:
            self.data_fetched.emit(data)

    def stop(self):
        self.running = False
        self.wait()