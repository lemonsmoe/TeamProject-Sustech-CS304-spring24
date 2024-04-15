from cryptography.fernet import Fernet
import json

# 课程信息的二维列表示例
# courses_data = [
#     ["数学", "周一", "张老师"],
#     ["物理", "周二", "李老师"],
#     ["化学", "周三", "王老师"]
# ]
#
# # 生成密钥并保存（只有知道密钥的人才能加密和解密）
# key = Fernet.generate_key()
# with open('secret.key', 'wb') as key_file:
#     key_file.write(key)
#
# # 用密钥创建Fernet对象
# cipher_suite = Fernet(key)
#
# # 序列化和加密数据
# serialized_data = json.dumps(courses_data).encode()
# encrypted_data = cipher_suite.encrypt(serialized_data)
#
# # 将加密后的数据保存到文件
# with open('courses_data.encrypted', 'wb') as encrypted_file:
#     encrypted_file.write(encrypted_data)

# 解密示例函数
def decrypt_data(key):
    # 在实际情况中，您可能需要更安全的验证密码的方式
    try:
        # with open('secret.key', 'rb') as key_file:
        #     key = key_file.read()
        # key = b'iImnalV464Rd89gPCDTjRqR5mLg3vTv4jtdFM8UO-Wk='
        cipher_suite = Fernet(key)
        with open('courses_data.encrypted', 'rb') as encrypted_file:
            encrypted_data = encrypted_file.read()
        decrypted_data = cipher_suite.decrypt(encrypted_data)
        courses_data = json.loads(decrypted_data.decode())
        return courses_data
    except Exception as e:
        print("解密失败：", e)
        return None


def main():
    # 测试解密功能
    password = input("请输入密码以访问课程信息：")
    key = b'iImnalV464Rd89gPCDTjRqR5mLg3vTv4jtdFM8UOWk='
    decrypted_courses = decrypt_data(key)
    if decrypted_courses:
        print("课程信息：")
        for course in decrypted_courses:
            print(course)