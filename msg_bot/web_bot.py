# Web自动控制


import os, time
from selenium import webdriver
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.action_chains import ActionChains

DEBUG = False

class WebBot:
    def __init__(self, user_data_dir="./user_data", driver_path=None, headless=False):
        self.user_data_dir = user_data_dir
        self.driver_path = driver_path
        # 设置使用默认数据目录
        self.options = Options()
        self.options.add_argument("--log-level=3")
        if headless:
            self.options.add_argument("--headless")  # 启用无头模式
        self.options.add_argument("--window-size=1920,1080")
        self.options.add_argument("--disable-gpu")  # 禁用 GPU 加速（在某些情况下可以解决布局问题）
        if self.user_data_dir is not None:
            self.options.add_argument(f"--user-data-dir={self.user_data_dir}")
        # 创建 EdgeService 对象
        if self.driver_path is not None:
            self.service = EdgeService(executable_path=self.driver_path)
        else:
            self.service = EdgeService()
        #self.options.add_argument("--window-size=1920,1080")
        # 启动 Edge 浏览器
        self.driver = webdriver.Edge(service=self.service, options=self.options)
        # 页面等待时间
        self.element_wait_time = 1

    # 内部使用接口-非必要不调用
    # 获取元素列表
    def get_elements(self, xpath, timeout=10):
        try:
            elements = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_all_elements_located((By.XPATH, xpath))
            )
        except TimeoutException:
            elements = []
        return elements

    # 获取单个元素
    def get_element(self, xpath, timeout=10):
        try:
            element = WebDriverWait(self.driver, timeout).until(
                EC.presence_of_element_located((By.XPATH, xpath))
            )
        except TimeoutException:
            element = None
        return element


    # 对外使用接口
    # 打开网页
    def open_url(self, url):
        try:
            self.driver.get(url)
            return True
        except:
            return False
        
    # 获取页面
    def get_page(self):
        return self.driver.current_window_handle
    
    # 切换页面
    def switch_page(self, page_name):
        try:
            self.driver.switch_to.window(page_name)
            return True
        except:
            return False
        
    # 刷新页面
    def refresh_page(self):
        try:
            self.driver.refresh()
            return True
        except:
            return False
        
    # 点击元素
    def click_element(self, element_xpath):
        try:
            element = self.get_element(element_xpath, self.element_wait_time)
            if element != None:
                element.click()
                return True
            else:
                if DEBUG:
                    print("找不到可点击的元素：" + element_xpath)
                return False
        except:
            if DEBUG:
                print("点击元素：" + element_xpath + "异常")
            return False
        
    # 鼠标悬停
    def move_to_element(self, element_xpath):
        try:
            # 找到需要鼠标悬浮的元素
            element = self.get_element(element_xpath, self.element_wait_time)
            if element != None:
                # 创建 ActionChains 对象
                actions = ActionChains(self.driver)
                # 将鼠标移动到该元素上
                actions.move_to_element(element).perform()
                return True
            else:
                return False
        except:
            return False
        
    # 获取内容
    def get_content(self, element_xpath):
        try:
            element = self.get_element(element_xpath, self.element_wait_time)
            if element != None:
                return element.text
            else:
                return None
        except:
            return None

    # 获取内容列表    
    def get_content_list(self, element_xpath):
        try:
            elements = self.get_elements(element_xpath, self.element_wait_time)
            if elements != []:
                return [element.text for element in elements]
            else:
                return []
        except:
            return []

    # 输入内容
    def input_content(self, element_xpath, content):
        try:
            element = self.get_element(element_xpath, self.element_wait_time)
            if element != None:
                element.send_keys(content)
                return True
            else:
                return False
        except:
            return False
        
    # 关闭浏览器
    def close_web(self):
        try:
            self.driver.quit()
            return True
        except:
            return False