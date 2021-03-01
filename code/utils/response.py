from datetime import datetime
from io import BytesIO
import typing

from django.http import HttpResponse
import xlwt


def generate_excel_response(
        excel_data: typing.List,
        excel_headers: typing.List = None,
        sheet_name: str = '',
        filename: str = '') -> HttpResponse:
    sheet_name = sheet_name or '1'
    filename = filename or datetime.now().strftime("%Y%m%d%H%M%S")

    http_response = HttpResponse()
    output = BytesIO()
    work_book = xlwt.Workbook(encoding="utf-8")
    work_sheet = work_book.add_sheet(sheet_name)

    offset = 0
    # 处理表头
    if excel_headers:
        for index, title in enumerate(excel_headers):
            work_sheet.write(0, index, title)
        offset = 1

    # 处理内容
    for row_num, row_data in enumerate(excel_data):
        for index, cell_data in enumerate(row_data):
            work_sheet.write(row_num + offset, index, cell_data)

    work_book.save(output)
    output.seek(0)
    http_response["Content-Type"] = "application/octet-stream"
    http_response["Content-Disposition"] = f'filename="{filename}.xls"'
    http_response.write(output.getvalue())
    return http_response
