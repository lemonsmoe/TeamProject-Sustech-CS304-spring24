在Python中模拟浏览器登录通常是通过发送HTTP请求实现的。这可以用几个不同的库完成，比如经典的`requests`库，或是更复杂的`selenium`库来控制一个真正的浏览器实例。

以下是如何使用`requests`库及其`Session`对象来保存cookie来模拟登录过程的步骤：

1. 首先，安装`requests`库（如果还没有安装的话）：

```bash
pip install requests
```

2. 使用`requests`模拟登录并获取cookies：

```python
import requests

# 创建一个Session对象，它会自动处理cookies
session = requests.Session()

# 登录页面的URL
login_url = "https://cas.sustech.edu.cn/cas/login?service=https%3A%2F%2Ftis.sustech.edu.cn%2Fcas"

# 登陆表单所需要的数据
payload = {
    'username': 'your_username',
    'password': 'your_password'
}

# 发送POST请求来模拟登录
response = session.post(login_url, data=payload)

# 检查是否登陆成功
if response.ok:
    # 登录后，Session对象中就保存了cookies
    cookies = session.cookies

    # 你现在可以使用session对象发送更多的请求，它会自动处理cookies
    # 例如：访问一个需要登录的页面
    profile_page = "http://example.com/profile"
    response = session.get(profile_page)

    # 打印页面内容
    print(response.text)
else:
    print("Login failed!")

# 获取cookie字典
cookie_dict = session.cookies.get_dict()
print(cookie_dict)
```

请记住将`example.com`、`your_username`和`your_password`替换为合适的值。

另外一种方法是用`selenium`库：

1. 安装`selenium`库和WebDriver（比如ChromeDriver或geckodriver）：

```bash
pip install selenium
```

2. 使用`webdriver`进行登录，并从中获取cookies：

```python
from selenium import webdriver

# 初始化webdriver实例（下面是chrome驱动，你需要下载对应的chromedriver）
driver = webdriver.Chrome('/path/to/chromedriver')

# 打开登录页面
driver.get("http://example.com/login")

# 定位用户名和密码输入框，并输入你的凭证
driver.find_element_by_id("username").send_keys("your_username")
driver.find_element_by_id("password").send_keys("your_password")

# 定位登录按钮并点击
driver.find_element_by_id("login_button").click()

# 等待页面加载完毕（需要根据实际情况调整）
driver.implicitly_wait(10)

# 获取cookies
cookies = driver.get_cookies()

# 打印出所有的cookie
for cookie in cookies:
    print(cookie)

# 关闭webdriver
driver.quit()
```

记得替换`/path/to/chromedriver`、`your_username`和`your_password`为实际情况的路径和登陆凭证，以及更新相应的元素定位符（如你的网站使用的`id`、`name`、`class`等）。

当使用`selenium`时，记得安装对应浏览器的WebDriver，如ChromeDriver或geckodriver，并确保它的路径正确。此外，`selenium`通常比`requests`慢，因为它会打开一个实际的浏览器窗口并在里面执行操作。但它更适合处理复杂的交互，例如模拟JavaScript行为或处理复杂的登录流程。