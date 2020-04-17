import xlrd


# 读excel
def read_excel(filePath):
    rexcel = xlrd.open_workbook(filePath)
    # 获取表格
    sheet = rexcel.sheet_by_index(0)
    row = 1
    while True:
        try:
            rows = sheet.row_values(row)

        except IndexError:
            break


