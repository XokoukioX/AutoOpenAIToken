from selenium import webdriver
import json
from bs4 import BeautifulSoup
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
import undetected_chromedriver as uc
import random
import os
import re

try:
    os.remove("token.txt")
except FileNotFoundError:
    print("没有Token.txt文件，跳过此步骤")
a = str(random.randint(1, 256))
b = str(random.randint(5, 758))
question = "计算：" + a + "*" + b + "= ?"
question = str(question)
print("将发送的问题为:" + question)

user_data_dir = r""#这里填写你的Chrome安装目录(e.g C:\Users\your_user_name\AppData\Local\Google\Chrome\User Data)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument('--start-maximized')  # 设置浏览器窗口大小
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

# chrome_options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
# chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 这里添加一些启动的参数
# chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消chrome受自动控制提示

driver = uc.Chrome(options=chrome_options)
print("打开灌水会话")
driver.get('https://chat.openai.com/c/')#这后面填写你的回话ID(e.g 75342f9f-3396-4a40-bt78-7234949a4bdd4)
print("发送问题")
WebDriverWait(driver, 20).until(EC.visibility_of_element_located(
    (By.XPATH, "/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/textarea"))).send_keys(question)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR,
                    r'#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > '
                    r'div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > '
                    r'div.flex.h-full.flex-col > '
                    r'div.w-full.pt-2.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border'
                    r'-transparent.md\:w-\[calc\(100\%-\.5rem\)\] > form > div > div > div > button > span > '
                    r'svg').click()
print("等待回复...")
time.sleep(4)
print("获取token")
driver.get('https://chat.openai.com/api/auth/session')
html = driver.page_source
soup = BeautifulSoup(html, 'html.parser')
json_data_str = soup.pre.string
json_data = json.loads(json_data_str)
access_token = json_data.get('accessToken')
print('accessToken的值:', access_token)

access_token_file_path = 'token.txt'

# 打开文件并写入accessToken的值
with open(access_token_file_path, 'w') as file:
    file.write(access_token)
print("保存为token.txt成功！")

file_path = r' '#这里填写机器人的cfg位置(e.g C:\Users\your_user_name\Desktop\Kawakaze\QBOT_\chatgpt-mirai-qq-bot\config.cfg)
# 显式指定使用UTF-8编码打开文件
with open(file_path, 'r', encoding='utf-8') as file:
    file_content = file.read()

# 在这之后，继续进行操作...
# 定义正则表达式模式，匹配access_token的值
pattern = re.compile(r'(access_token\s*=\s*")[^"]+(")')

# 使用正则表达式查找匹配的文本
match = pattern.search(file_content)

if match:
    # 获取匹配到的access_token的值
    old_access_token = match.group(1)  # 使用 group(1) 获取括号内的部分

    # 新的access_token的值
    new_access_token = access_token

    # 替换access_token的值
    file_content = pattern.sub(rf'\g<1>{new_access_token}\g<2>', file_content)

    # 将替换后的内容写回文件
    with open(file_path, 'w', encoding='utf-8') as file:
        file.write(file_content)

    print(f'文件 {file_path} 中的 access_token 已被替换。')
    driver.stop_client()
else:
    print('未找到匹配的 access_token。')
