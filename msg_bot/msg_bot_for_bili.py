# Bilibili Auto Reply Bot

import os
import time
import sys
sys.path.append("msg_bot")

import reply_config
from web_bot import WebBot

# 固定回复前缀
fan_fixed_reply_prefix = "【MessageBot自动回复测试】"
non_fan_fixed_reply_prefix = "【MessageBot自动回复测试】"


class MessageBotForBili:
    def __init__(self):
         # 获取当前工作目录
        self.current_dir = os.getcwd()
        # 日志目录
        self.log_dir = os.path.join(self.current_dir, "logs")
        # 确保日志文件夹存在
        os.makedirs(self.log_dir, exist_ok=True)
        # 构造日志文件名，包含时间戳
        timestamp = time.strftime('%Y-%m-%d_%H-%M-%S', time.localtime(time.time()))
        self.log_file = os.path.join(self.log_dir, f"log_msg_bot_{timestamp}.txt")
        # 指定用户数据目录
        self.user_data_dir = os.path.join(self.current_dir, "user_data")
        # 指定 Edge 驱动的路径
        self.driver_path = os.path.join(self.current_dir, "driver", "msedgedriver.exe")

        # 页面元素
        # 登录头像
        self.element_xpath_login = "//li[@class='right-entry-item']/li[@class='v-popover-wrap']"
        # 用户头像
        self.element_xpath_user = "//li[@class='v-popover-wrap header-avatar-wrap']"
        # 消息
        self.element_xpath_message = "//li[@class='v-popover-wrap right-entry__outside right-entry--message']"
        # 粉丝列表
        self.element_xpath_fans_list = "//div[@class='nav-statistics']//a[contains(@href, '/relation/fans')]/span[@class='nav-statistics__item-num']"
        # 粉丝数
        self.element_xpath_fans_num = "//div[@class='counts-item']//a[contains(@href, '/fans/fans')]/div[@class='count-num']"
        # 粉丝名称
        self.element_xpath_fans_name = "//div[@class='relation-card-info']//a[@class='relation-card-info__uname' or @class='relation-card-info__uname vip']/div"
        # 粉丝页面 下一页
        self.element_xpath_fans_next = "//button[@class='vui_button vui_pagenation--btn vui_pagenation--btn-side' and text()='下一页']"
        # 未关注人消息提示
        self.element_xpath_unfollow_msg_tip = "//div[@data-id='group_1']/div[@class='_SessionItem__Notification_dnmx0_114']"
        # 未读消息提示
        self.element_xpath_unread_msg_tips = "//div[@class='_SessionItem__Notification_dnmx0_114']/div[@class='_SessionItem__NotificationNumber_dnmx0_124']"
        # 我的消息
        self.element_xpath_my_msg = "//div[@class='message-sidebar__item-name' and text()='我的消息']"
        # 对话方名称
        self.element_xpath_contact_name = "//div[@class='_ContactName_1lacc_26']"
        # 最新消息
        self.element_xpath_latest_msg = "//div[@class='_MsgText_igf38_1']/div[@class='_MsgText__Content_igf38_19']/div[@class='_RichText_19yqs_1']/span"
        # 发送消息框
        self.element_xpath_send_msg_box = "//div[@class='brt-root']/div[@class='brt-editor']"
        # 发生消息按键
        self.element_xpath_send_msg_btn = "//div[@class='_MessageSendBox__SendBtn_125bg_58' and text()='发送']"
        
        # 页面
        self.main_page = None
        self.fans_page = None 
        self.message_page = None

        # 固定回复前缀
        self.fan_fixed_reply_prefix = fan_fixed_reply_prefix
        self.non_fan_fixed_reply_prefix = non_fan_fixed_reply_prefix
        print("-"*16)
        print("B站消息机器人")
        print("-"*16)
        # 初始化
        self.system_init()

    # 日志打印
    def log_print(self, log_str):
        log_txt = f"[{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))}] {log_str}"
        print(log_txt)
        # 打开日志文件并写入日志内容
        with open(self.log_file, 'a', encoding='utf-8') as file:
            file.write(log_txt+"\n")
            
    # 登录相关接口
    # 检查登录
    def check_login(self, web_bot, timeout=1):
        try:
            # 确认是否登录
            if web_bot.get_element(self.element_xpath_user, timeout) != None:
                # 已登录
                return True
            else:
                return False
        except:
            return False
        
    # 登录
    def login(self):
        # 打开登录页面
        web_bot_login = WebBot(user_data_dir=self.user_data_dir, driver_path=self.driver_path, headless=False)
        web_bot_login.open_url("https://www.bilibili.com/")
        if web_bot_login.click_element(self.element_xpath_login):
            # 登录需要时间，默认超时120秒
            self.log_print("登录页面已打开,请在120秒内完成登录")
            if self.check_login(web_bot_login, 120):
                self.log_print("登录成功")
                web_bot_login.close_web()
                return True
            else:
                self.log_print("登录失败")
                web_bot_login.close_web()
                return False
        else:
            self.log_print("登录异常")
            web_bot_login.close_web()
            return False


    # 粉丝相关接口
    # 打开粉丝页面
    def open_fans_page(self):
        # 打开个人中心页面
        if self.web_bot.click_element(self.element_xpath_user):
            # 个人中心页面
            self.log_print("已打开个人中心页面")
            temp_page = self.web_bot.driver.window_handles[-1]
            self.web_bot.switch_page(temp_page)
            # 点击粉丝列表
            if self.web_bot.click_element(self.element_xpath_fans_list):
                try:
                    self.fans_num = int(self.web_bot.get_content(self.element_xpath_fans_list))
                except:
                    self.log_print("获取粉丝数失败")
                    self.fans_num = 0
                # 粉丝页面
                self.fans_page = self.web_bot.driver.window_handles[-1]
                return self.web_bot.switch_page(self.fans_page)
            else:
                self.log_print("??")
                return False
        else:
            return False

    # 粉丝是否发生变化
    def is_fans_change(self):
        if self.fans_num != self.get_fans_num():
            return True
        else:
            return False

    # 粉丝判断
    def is_fan(self, user_name):
        if user_name in self.fans_list:
            return True
        else:
            return False

    # 获取粉丝数
    def get_fans_num(self):
        # 切换消息页面
        self.web_bot.switch_page(self.message_page)
        # 刷新页面
        #self.driver.refresh()
        # 鼠标悬停
        self.web_bot.move_to_element(self.element_xpath_user)
        time.sleep(1.0)
        # 获取粉丝数
        fans_num = self.web_bot.get_content(self.element_xpath_fans_num)
        if fans_num != None:
            try:
                fans_num = int(fans_num)
                return int(fans_num)
            except:
                self.log_print("获取粉丝数失败")
                return 0
        else:
            self.log_print("获取粉丝数失败")
            return 0

    # 获取粉丝列表
    def get_fans_list(self):
        fans_list = []
        try:
            # 切换粉丝页面
            self.web_bot.switch_page(self.fans_page)
            # 刷新页面
            self.web_bot.refresh_page()
            # 粉丝列表
            fans_list = self.web_bot.get_content_list(self.element_xpath_fans_name)
            # 循环点击下一页遍历粉丝列表
            while self.web_bot.click_element(self.element_xpath_fans_next):
                fans_list.extend(self.web_bot.get_content_list(self.element_xpath_fans_name))
            #self.log_print(f"粉丝列表: {fans_list}")
            #self.log_print(f"粉丝数量: {len(fans_list)}")
        except Exception as e:
            self.log_print(f"更新粉丝列表失败: {e}")
        return fans_list

    # 更新粉丝列表
    def update_fans_list(self):
        self.fans_list = self.get_fans_list()
        self.fans_num = self.get_fans_num()
        if len(self.fans_list) == self.fans_num:
            # self.fans_num = len(self.fans_list)
            return True
        else:
            return False


    # 消息相关接口
    # 打开消息页面
    def open_message_page(self):
        # 打开消息页面
        if self.web_bot.click_element(self.element_xpath_message):
            # 消息页面
            self.message_page = self.web_bot.driver.window_handles[-1]
            return self.web_bot.switch_page(self.message_page)
        else:
            return False
   
    # 是否有新消息
    def is_new_message(self):
        # 切换消息页面
        self.web_bot.switch_page(self.message_page)
        # 刷新页面
        #self.web_bot.refresh_page()
        # 点击我的消息
        self.web_bot.click_element(self.element_xpath_my_msg)
        # 未关注人消息
        if self.web_bot.get_element(self.element_xpath_unfollow_msg_tip, timeout=1) != None:
            # 有未关注人消息提示
            return True
        # 未读消息
        if self.web_bot.get_element(self.element_xpath_unread_msg_tips, timeout=1) != None:
            return True
        # 无新消息
        return False

    # 进入到最新消息对话
    def enter_new_message_chat(self):
        # 切换消息页面
        self.web_bot.switch_page(self.message_page)
        # 刷新页面
        #self.web_bot.refresh_page()
        # 点击我的消息
        if self.web_bot.click_element(self.element_xpath_my_msg) == False:
            self.log_print("点击我的消息失败")
            return False
        # 未关注人新消息
        if self.web_bot.get_element(self.element_xpath_unfollow_msg_tip, timeout=1) != None:
            # 点击未关注人消息
            self.web_bot.click_element(self.element_xpath_unfollow_msg_tip)
            self.log_print("进入到未关注人消息页面")
        # 点击未读消息
        return self.web_bot.click_element(self.element_xpath_unread_msg_tips)

    # 获取对方名称
    def get_contact_name(self):
        return self.web_bot.get_content(self.element_xpath_contact_name)

    # 获取最新消息
    def get_lastest_message(self):
        # 只获取最新一条消息
        return self.web_bot.get_content(self.element_xpath_latest_msg)

    # 自定义回复
    def customer_reply(self, message):
        # 自定义回复逻辑
        if message == "自定义消息":
            self.customer_reply_message = message
            # 置True则回复自定义消息
            return True
        return False

    # 获取粉丝回复消息
    def get_fans_reply_message(self, message):
        # 将输入消息转换为小写
        message_lower = message.lower()
        # 可在此处添加自定义的处理逻辑
        if self.customer_reply(message_lower):
            return self.customer_reply_message
        # 完全匹配（忽略大小写）
        for key in reply_config.fans_complete_dict.keys():
            if message_lower == key.lower():
                reply_message = reply_config.fans_complete_dict[key]
                return reply_message
        # 关键字匹配（忽略大小写）
        for key, value in reply_config.fans_keyword_dict.items():
            if key.lower() in message_lower:
                return value
        # 其他情况
        return reply_config.fans_other_dict["default"]

    # 获取非粉丝回复消息
    def get_non_fans_reply_message(self, message):
        # 将输入消息转换为小写
        message_lower = message.lower()
        # 完全匹配（忽略大小写）
        for key in reply_config.non_fans_complete_dict.keys():
            if message_lower == key.lower():
                reply_message = reply_config.non_fans_complete_dict[key]
                return reply_message
        # 关键字匹配（忽略大小写）
        for key, value in reply_config.non_fans_keyword_dict.items():
            if key.lower() in message_lower:
                return value
        
        # 其他情况
        return reply_config.non_fans_other_dict["default"]

    # 回复消息
    def reply_message(self):
        # 获取对方名称
        contact_name = self.get_contact_name()
        if contact_name is None:
            self.log_print("获取对方名称失败")
            return False
        self.log_print(f"对方名称: {contact_name}")
        # 获取最新的消息
        lastest_msg = self.get_lastest_message()
        if lastest_msg is None:
            self.log_print("获取最新消息失败")
            return False
        self.log_print(f"最新消息: {lastest_msg}")
        if self.is_fan(contact_name):
            # 粉丝
            self.log_print("对方身份：粉丝")
            reply_msg = self.fan_fixed_reply_prefix + self.get_fans_reply_message(lastest_msg)
        else:
            # 非粉丝
            self.log_print("对方身份：非粉丝")
            reply_msg = self.non_fan_fixed_reply_prefix + self.get_non_fans_reply_message(lastest_msg)
        # 根据消息内容回复
        if self.web_bot.input_content(self.element_xpath_send_msg_box, reply_msg):
            self.log_print(f"回复消息: {reply_msg}")
        else:
            self.log_print("输入消息失败")
            return False
        # 发送消息
        if self.web_bot.click_element(self.element_xpath_send_msg_btn):
            self.log_print("发送消息成功")
            return True
        else:
            self.log_print("发送消息失败")
            return False


    # 系统初始化
    def system_init(self):
        self.log_print("系统初始化...")
        # 创建网页机器人(无头模式)
        self.web_bot = WebBot(user_data_dir=self.user_data_dir, driver_path=self.driver_path, headless=True)
        # 打开主页
        self.web_bot.open_url("https://www.bilibili.com/")
        # 检测是否是登陆状态
        self.log_print("检测是否是登陆状态...")
        if self.check_login(self.web_bot):
            self.log_print("当前已经登录")
            # 主页面
            self.main_page = self.web_bot.get_page()
        else:
            self.log_print("当前未登录，需要登录")
            self.web_bot.close_web()
            # 登录
            while not self.login():
                self.log_print("登录未完成，请重新尝试")
            self.log_print("登录已完成")
            # 重新打开网页
            self.web_bot = WebBot(user_data_dir=self.user_data_dir, driver_path=self.driver_path, headless=True)
            self.web_bot.open_url("https://www.bilibili.com/")
            self.main_page = self.web_bot.get_page()
        # 打开粉丝页面
        if self.open_fans_page():
            self.log_print("打开粉丝页面成功")
        else:
            self.log_print("打开粉丝页面失败,初始化中止")
            return False
        # 打开消息页面
        if self.open_message_page():
            self.log_print("打开消息页面成功")
        else:
            self.log_print("打开消息页面失败,初始化中止")
            return False
        # 更新粉丝列表
        self.fans_list = []
        if self.update_fans_list() == False:
            self.log_print("初始化粉丝列表失败,初始化中止")
            return False
        self.log_print(f"当前粉丝数量: {self.fans_num}")
        self.log_print(f"当前粉丝列表: {self.fans_list}")
        self.log_print("系统初始化完成")
        # 初始化成功
        return True

    # 自动回复引擎
    def auto_reply_engine(self):
        self.log_print("自动回复引擎启动")
        count = 0
        try:
            while True:
                count += 1
                self.log_print("================")
                self.log_print(f"第{count}次检测")
                # 检查是否有未读消息
                if self.is_new_message():
                    self.log_print("检测到有新消息")
                    # 检查粉丝数量是否发生变化
                    if self.is_fans_change():
                        self.log_print("粉丝数量发生变化")
                        # 更新粉丝列表
                        if self.update_fans_list():
                            self.log_print("更新粉丝列表成功")
                            self.log_print(f"当前粉丝数量: {self.fans_num}")
                        else:
                            self.log_print("更新粉丝列表失败")
                    # 进入未读消息对话
                    if self.enter_new_message_chat():
                        self.log_print("进入到未读消息对话")
                        # 回复消息
                        if self.reply_message():
                            self.log_print("回复消息成功")
                        else:
                            self.log_print("回复消息失败")
                        # 退出对话窗口
                        # 点击我的消息
                        if self.web_bot.click_element(self.element_xpath_my_msg):
                            self.log_print("退出对话窗口成功")
                        else:
                            self.log_print("退出对话窗口失败")
                else:
                    self.log_print("无新消息")
                    # 检查粉丝数量是否发生变化
                    if self.is_fans_change():
                        self.log_print("粉丝数量发生变化")
                        # 更新粉丝列表
                        if self.update_fans_list():
                            self.log_print("更新粉丝列表成功")
                            self.log_print(f"当前粉丝数量: {self.fans_num}")
                        else:
                            self.log_print("更新粉丝列表失败")
        except Exception as e:
            self.log_print(f"自动回复引擎异常: {e}")
            self.log_print("自动回复引擎退出")
            self.web_bot.close_web()


# 使用示例
if __name__ == "__main__":
    msg_bot = MessageBotForBili()
    msg_bot.auto_reply_engine()
