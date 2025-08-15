from binance.client import Client
from binance.exceptions import BinanceAPIException
from PyQt6.QtCore import QObject, pyqtSignal


class BinanceClient(QObject):
    data_updated = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, api_manager):
        super().__init__()
        self.api_manager = api_manager
        self.client = None
        self.running = False

    def connect(self):
        """连接到币安API"""
        api_key, api_secret = self.api_manager.get_api()
        if not api_key or not api_secret:
            self.error_occurred.emit("无效的API密钥")
            return False

        try:
            self.client = Client(api_key, api_secret)
            return True
        except BinanceAPIException as e:
            self.error_occurred.emit(f"API连接错误: {e.message}")
            return False

    def get_holdings(self):
        """获取当前持仓数据"""
        if not self.client:
            if not self.connect():
                return None

        try:
            account = self.client.get_account()
            balances = account['balances']

            prices = {ticker['symbol']: float(ticker['price'])
                      for ticker in self.client.get_all_tickers()}

            holdings = []
            total_value = 0.0

            for balance in balances:
                asset = balance['asset']
                amount = float(balance['free']) + float(balance['locked'])

                if amount > 0:
                    value = 0.0

                    if asset in ['USDT', 'BUSD', 'USDC']:
                        value = amount
                    else:
                        symbol = f"{asset}USDT"
                        if symbol in prices:
                            value = amount * prices[symbol]

                    if value > 0:
                        holdings.append({
                            'asset': asset,
                            'amount': amount,
                            'value': value
                        })
                        total_value += value

            for item in holdings:
                item['percentage'] = (item['value'] / total_value) * 100

            return {
                'total_value': total_value,
                'holdings': holdings,
                'timestamp': account['updateTime']
            }

        except BinanceAPIException as e:
            error_message = f"API错误: {e.message}, 错误代码: {e.code}, 请求参数: {e.request_params}"
            self.error_occurred.emit(error_message)
            return None
        except Exception as e:
            self.error_occurred.emit(f"未知错误: {str(e)}")
            return None

        # 修正百分比计算逻辑
        for item in mock_data['holdings']:
            if mock_data['total_value'] > 0 and item['value'] >= 0:
                item['percentage'] = (item['value'] / mock_data['total_value']) * 100
            else:
                item['percentage'] = 0.0  # 处理零/负值

        return mock_data