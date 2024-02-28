import openpyxl


class ExcelHandler:

    def __init__(self, path):
        # path是excel文件所在的路径，初始化对象传入路径即可
        self.path = path
        self.workbook = None

    def get_workbook(self):
        # 创建workbook对象
        workbook = openpyxl.load_workbook(self.path)
        self.workbook = workbook
        return workbook

    def get_sheet(self, name):
        # 创建sheet对象
        work_book = self.get_workbook()
        worksheet = work_book[name]
        return worksheet

    def read_sheet(self, name):
        sheet = self.get_sheet(name)
        all_rows = list(sheet.rows)
        # 获取第一行表头的值
        headers = []
        for title in all_rows[0]:
            headers.append(title.value)
        # 获取第二行开始的值
        data = []
        for row in all_rows[1:]:
            row_data = {}
            # 获取每行中的每个cell的索引和值，和表头拼接
            for idx, cell in enumerate(row):
                row_data[headers[idx]] = cell.value
            data.append(row_data)
        return data



