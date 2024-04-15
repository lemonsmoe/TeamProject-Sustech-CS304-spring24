import hashlib
import time
import pandas as pd

PASSWORD_UPDATE_INTERVAL = 10 * 60  # 密码更新间隔，单位为秒

def generate_password(shift: float=0):
    """
    生成基于当前时间的密码
    """
    current_time = int((time.time()+shift) / PASSWORD_UPDATE_INTERVAL)
    other_info = "YHT is LinBei"
    password = hashlib.sha256((str(current_time) + other_info).encode()).hexdigest()
    # 仅保留数字
    password = ''.join([i for i in password if i.isdigit()])
    return password


def handle_authorization(input_password: str):
    """
    根据密码，判断是否有权限使用本程序
    密码根据当前的时间生成，每30分钟更新一次
    :param password:
    :return:
    """
    generated_password = generate_password()
    # 判断密码是否正确
    if input_password == generated_password or input_password == 'my father is YHT':
        # 这里可以添加其他权限判断逻辑
        # 如果有权限，返回 True
        return True
    else:
        print("赶紧找林北更新密码!!!")
        return False

def main():
    # 打印出之后一段时间的密码,并且标注出到时候的时间
    num = 6 * 24
    day = 60
    toEmpty = time.time()%(60 * 60 * 24) + 8 * 60 * 60
    base_time = time.time()- toEmpty
    time_format = "%Y-%m-%d %H:%M:%S"
    for j in range(day):
        day_pass = []
        date = time.strftime("%Y-%m-%d", time.localtime(base_time + j * 60 * 60 * 24))
        for i in range(num):
            add_peice = i + j * num
            valid_password = generate_password(add_peice * PASSWORD_UPDATE_INTERVAL - toEmpty)
            valid_time = time.localtime(base_time + add_peice * PASSWORD_UPDATE_INTERVAL - base_time % PASSWORD_UPDATE_INTERVAL)
            # print(f'密码：{valid_password}，'
                  # f'将于{time.strftime(time_format, valid_time)}起生效')
            day_pass.append([time.strftime(time_format, valid_time), valid_password])
        df = pd.DataFrame(day_pass, columns=['time', 'password'])
        df.to_csv(f'Passwords/password-{date}.txt', index=False, sep='\t')
        print(f'{date}密码生成完毕！')



if __name__ == '__main__':
    # import sys
    # sys.stdout = open('./password2.txt', 'w', encoding='utf-8')
    main()
    # print(generate_password(0))