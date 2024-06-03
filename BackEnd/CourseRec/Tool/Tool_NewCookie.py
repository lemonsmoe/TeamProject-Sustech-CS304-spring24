import os.path
import time
import json
from time import sleep

from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from webdriver_manager.microsoft import EdgeChromiumDriverManager

def get_userinfo():
    with open('../Input/input.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
        username = data['login_username']
        password = data['login_password']
        return username, password

def get_new_Cookie():
    start = time.time()
    username, password = get_userinfo()
    # 设置Options
    options = webdriver.edge.options.Options()
    arguments = ' '.join(
        ['--disable-gpu', '--disable-dev-shm-usage', '--disable-extensions', '--no-sandbox', '--disable-infobars',
         '--headless'])
    options.add_argument(arguments)
    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
    print(f'初始化浏览器用时：{time.time() - start}秒')
    login_url = 'https://tis.sustech.edu.cn/authentication/main'
    # 打开登录页面
    driver.get(login_url)
    sleep(0.1)
    driver.find_element('class name', 'signmain_icon_wrap').find_element('tag name', 'img').click()
    # 等待 5 秒
    sleep(0.1)
    input_username = driver.find_element('id', 'username')
    input_username.send_keys(username)
    sleep(0.1)
    input_password = driver.find_element('id', 'password')
    input_password.send_keys(password)
    sleep(0.1)
    # print(driver.page_source)
    button_login = driver.find_elements('class name', 'mdc-button.mdc-button--raised')[1]
    print(button_login.text)
    button_login.click()
    sleep(0.1)
    print(f'点击登录前用时：{time.time() - start}秒')
    # 等待页面加载完毕（需要根据实际情况调整）
    driver.implicitly_wait(3)
    # 获取cookies
    cookies = driver.get_cookies()
    # 打印出所有的cookie
    coo = {}
    for cookie in cookies:
        print(cookie['name'], cookie['value'])
        coo[cookie['name']] = cookie['value']

    # 保存coo到文件
    with open('../CourseData/cookies.json', 'w', encoding='utf-8') as f:
        json.dump(coo, f, ensure_ascii=False)
    # 关闭webdriver
    driver.quit()
    print(f'总共用时：{time.time() - start}秒')


if __name__ == '__main__':
    get_new_Cookie()
