#coding=utf-8

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0

import  time
import  sys

print(sys.maxunicode)
myusername = "your_user_name"#帐号
mypassword = "your_password"#密码

#开启浏览器驱动
driver = webdriver.Chrome()
driver.implicitly_wait(10)
#打开网址
driver.get("http://www.smzdm.com/")
#窗口最大化
#driver.maximize_window()
#寻找登录按钮并且点击
#driver.find_element_by_id('navBar_login').click()
driver.find_element_by_css_selector("a[class='J_login_trigger']").click()
#多层窗口定位
driver.switch_to_frame('J_login_iframe')
#输入用户名
driver.find_element_by_id("username").send_keys(myusername)
#driver.find_element_by_css_selector("input[name='username']").send_keys(myusername)
#输入密码
driver.find_element_by_id("password").send_keys(mypassword)
#driver.find_element_by_css_selector("input[name='password']").send_keys(mypassword)
#点击登录
#driver.find_element_by_id('login_submit').click()
driver.find_element_by_css_selector("input[id='login_submit']").click()
#time.sleep(5)

print('start wait')
#WebDriverWait(driver,3).until(lambda driver : driver.find_element_by_id('navBar_login_Info').is_displayed()==True)
WebDriverWait(driver,3).until(lambda driver : driver.find_element_by_css_selector("div[class='user-info J_info']").is_displayed()==True)
print('end wait')
#webElement = driver.find_element_by_id('user_info_tosign')
webElement = driver.find_element_by_css_selector("a[class='J_punch']")
if(webElement.text =='签到领积分'):
    webElement.click()
else:
    print(webElement.text)

time.sleep(5)

#退出驱动
driver.quit()