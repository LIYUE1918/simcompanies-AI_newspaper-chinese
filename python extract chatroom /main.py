from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys  # 导入 Keys
import time
import requests
from webdriver_manager.chrome import ChromeDriverManager

# 设置Chrome选项
chrome_options = Options()
chrome_options.add_argument("--headless")  # 如果不需要打开实际的浏览器窗口
chrome_options.add_argument("--disable-gpu")

# 使用webdriver-manager自动管理ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

def login_sim_companies():
    """
    使用Selenium模拟登录Sim Companies网站
    """
    try:
        # 访问登录页面
        driver.get("https://www.simcompanies.com/signin/")

        # 等待页面加载并找到输入框 (增加了显式等待，更长的超时时间)
        wait = WebDriverWait(driver, 10) # 增加等待时间到20秒

        # 使用XPath来定位元素 (根据你提供的HTML结构)
        email_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="email"]')))
        password_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@name="password"]')))
       
        # 输入登录信息
        email_field.send_keys("example")  # 替换为你的用户名
        password_field.send_keys("example")  # 替换为你的密码

        # 提交表单 (使用Keys.RETURN)
        password_field.send_keys(Keys.RETURN)

        # 更长的等待时间，确保页面完全加载
        time.sleep(10)  # 等待登录完成, 增加到10秒

        # 获取登录后的cookies
        cookies = driver.get_cookies()
        session_cookies = {cookie['name']: cookie['value'] for cookie in cookies}
        print("登录成功，已获取cookies！")
        return session_cookies
    except Exception as e:
        print(f"登录时出现问题: {e}")
        # 打印页面源码以便调试
        print("Page Source:", driver.page_source) #  打印页面源码
        return None

def fetch_api_data(api_url, cookies):
    """
    使用获取到的Cookies访问受保护的API
    """
    try:
        # 使用登录后的cookies发起API请求
        response = requests.get(api_url, cookies=cookies)
        if response.status_code == 200:
            print("API数据获取成功！")
            return response.json()  # 返回API响应的JSON数据
        else:
            print(f"API请求失败，状态码: {response.status_code}")
    except requests.exceptions.RequestException as e:
        print(f"请求出现异常: {e}")
    return None

# 使用Selenium模拟登录
cookies = login_sim_companies()

# 如果登录成功，使用获取到的cookies访问API
if cookies:
    api_url = "https://www.simcompanies.com/api/chatroom/?chatroom=N&last_id=1000000000"
    data = fetch_api_data(api_url, cookies)
    if data:
        print("获取到的数据：")
        print(data)

# 关闭浏览器
driver.quit()
