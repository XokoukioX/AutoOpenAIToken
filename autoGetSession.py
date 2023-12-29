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

try:
    os.remove("token.txt")
except FileNotFoundError:
    print("没有Token.txt文件，跳过此步骤")
a = str(random.randint(1,256))
b = str(random.randint(5,758))
question = "计算：" + a + "*" + b + "= ?"
question = str(question)
print("将发送的问题为:" + question)

user_data_dir = r"C:\Users\zymooll\AppData\Local\Google\Chrome\User Data"

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_experimental_option("detach", True)  # 不要自动关闭浏览器
#chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 这里添加一些启动的参数
chrome_options.add_argument('--start-maximized')  # 设置浏览器窗口大小
#chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])  # 取消chrome受自动控制提示
chrome_options.add_argument('--profile-directory=Profile 1')
chrome_options.add_argument(f'--user-data-dir={user_data_dir}')

driver = uc.Chrome(options=chrome_options)
print("打开灌水会话")
driver.get('https://chat.openai.com/c/74c3bf9f-3396-4aa0-b478-726949a4bdd4')
print("发送问题")
WebDriverWait(driver,20).until(EC.visibility_of_element_located((By.XPATH,"/html/body/div[1]/div[1]/div[2]/main/div[2]/div[2]/form/div/div/div/textarea"))).send_keys(question)
time.sleep(1)
driver.find_element(By.CSS_SELECTOR,r'#__next > div.relative.z-0.flex.h-full.w-full.overflow-hidden > div.relative.flex.h-full.max-w-full.flex-1.flex-col.overflow-hidden > main > div.flex.h-full.flex-col > div.w-full.pt-2.md\:pt-0.dark\:border-white\/20.md\:border-transparent.md\:dark\:border-transparent.md\:w-\[calc\(100\%-\.5rem\)\] > form > div > div > div > button > span > svg').click()
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