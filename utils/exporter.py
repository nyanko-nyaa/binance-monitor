import pandas as pd
from datetime import datetime


def export_data(data, file_path, file_format, options, progress_callback=None):
    try:
        holdings = data['holdings']

        if options['only_nonzero']:
            holdings = [h for h in holdings if h['value'] > 0]

        export_data = []
        total = len(holdings)

        for idx, item in enumerate(holdings):
            export_item = {
                '币种': item['asset'],
                '持仓量': item['amount'],
                '占比 (%)': item['percentage']
            }

            if options['include_calc']:
                export_item['当前价格'] = item['value'] / item['amount'] if item['amount'] > 0 else 0
                export_item['总价值 (USDT)'] = item['value']

            export_data.append(export_item)

            if progress_callback:
                progress_callback(int(((idx + 1) / total) * 100))

        df = pd.DataFrame(export_data)

        df.loc['总计'] = [''] * (len(df.columns) - 1) + [data['total_value']]

        metadata = [
            f"导出时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}",
            f"账户总价值: ${data['total_value']:,.2f}",
            f"更新时间: {datetime.fromtimestamp(data['timestamp'] / 1000).strftime('%Y-%m-%d %H:%M:%S')}"
        ]

        if file_format == "csv":
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write("\n".join(metadata) + "\n\n")
                df.to_csv(f, index=False)
        else:
            # 明确指定引擎和文件扩展名
            if not file_path.endswith('.xlsx'):
                file_path += '.xlsx'

            with pd.ExcelWriter(
                    file_path,
                    engine='openpyxl',
                    mode='w',
            ) as writer:
                df.to_excel(writer, sheet_name='持仓数据', index=False)

                # 添加元数据
                workbook = writer.book
                sheet = workbook['持仓数据']
                for i, meta in enumerate(metadata):
                    sheet.cell(row=i + 1, column=len(df.columns) + 2, value=meta)

        return True
    except Exception as e:
        print(f"导出错误: {str(e)}")
        return False