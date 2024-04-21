# 首先安装所需库
# pip install msoffcrypto-tool openpyxl pandas

import msoffcrypto
import openpyxl
import io
import pandas as pd
import win32com.client


def read_encrypt_excel(file_path, password):
    # 打开并解密文件
    file = msoffcrypto.OfficeFile(open(file_path, "rb"))
    # 创建一个内存中的文件对象
    decrypted_stream = io.BytesIO()
    file.load_key(password=password)  # 使用密码解锁
    file.decrypt(decrypted_stream)
    # 内存中的文件对象可以使用openpyxl或pandas来处理
    wb = openpyxl.load_workbook(decrypted_stream)
    sheet = wb.active
    # 例如，使用pandas读取为DataFrame
    df = pd.read_excel(decrypted_stream)
    return df


def pwd_xlsx(old_filename, new_filename, pwd_str, pw_str=''):
    xcl = win32com.client.Dispatch("Excel.Application")
    # pw_str为打开密码, 若无 访问密码, 则设为 ''
    wb = xcl.Workbooks.Open(old_filename, False, False, None, pw_str)
    xcl.DisplayAlerts = False

    # 保存时可设置访问密码.
    wb.SaveAs(new_filename, None, pwd_str, '')
    print('加密完成！')

    xcl.Quit()
