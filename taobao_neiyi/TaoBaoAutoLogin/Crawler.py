# -*- coding:UTF-8 -*-
import time
from datetime import date, timedelta
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
TB_LOGIN_URL = 'https://login.taobao.com/member/login.jhtml'
# TB_LOGIN_URL = 'https://login.taobao.com/member/login.jhtml?sub=true&style=miniall&from=subway&full_redirect=true&newMini2=true&tpl_redirect_url=//subway.simba.taobao.com/entry/login.htm'
CHROME_DRIVER = r"D:\Loading_environment\chromedriver.exe"

class SessionException(Exception):
    """
    会话异常类
    """
    def __init__(self, message):
        super().__init__(self)
        self.message = message

    def __str__(self):
        return self.message


class Crawler:

    def __init__(self):
        self.browser = None
        self.yesterday_date = None
        self.today_date = None
        self.html_source = None

    def start(self, username, password):

        print("初始化日期")
        self.__init_date()
        print("初始化浏览器")
        self.__init_browser()
        print("切换至密码输入框")
        self.__switch_to_password_mode()
        time.sleep(0.5)
        print("输入用户名")
        self.__write_username(username)
        time.sleep(2.5)
        print("输入密码")
        self.__write_password(password)
        time.sleep(3.5)
        print("程序模拟解锁")
        if self.__lock_exist():
            self.__unlock()
        print("开始发起登录请求")
        self.__submit()
        time.sleep(4.5)
        # 登录成功，直接请求页面
        print("登录成功，跳转至目标页面")
        self.__navigate_to_target_pagevigate_to_target_page()
        # time.sleep(6.5)
        print("解析页面文本")
        crawler_list = self.__parse_page_content()
        #
        # 连接数据库并保存数据
        print("保存数据到mysql数据库")
        self.__save_list_to_db(crawler_list)

    def __switch_to_password_mode(self):
        """
        切换到密码模式
        :return:
        """
        if self.browser.find_element_by_id('J_QRCodeLogin').is_displayed():
            self.browser.find_element_by_id('J_Quick2Static').click()

    def __write_username(self, username):
        """
        输入账号
        :param username:
        :return:
        """
        username_input_element = self.browser.find_element_by_id('TPL_username_1')
        username_input_element.clear()
        username_input_element.send_keys(username)

    def __write_password(self, password):
        """
        输入密码
        :param password:
        :return:
        """
        password_input_element = self.browser.find_element_by_id("TPL_password_1")
        password_input_element.clear()
        password_input_element.send_keys(password)

    def __lock_exist(self):
        """
        判断是否存在滑动验证
        :return:
        """
        return self.__is_element_exist('#nc_1_wrapper') and self.browser.find_element_by_id(
            'nc_1_wrapper').is_displayed()

    def __unlock(self):
        """
        执行滑动解锁
        :return:
        """
        bar_element = self.browser.find_element_by_id('nc_1_n1z')
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 300, 0).perform()
        time.sleep(0.1)
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 600, 0).perform()
        time.sleep(0.2)
        ActionChains(self.browser).drag_and_drop_by_offset(bar_element, 800, 0).perform()
        time.sleep(0.3)
        # ActionChains(self.browser).click_and_hold(on_element=bar_element).perform()
        # time.sleep(0.15)
        # ActionChains(self.browser).move_to_element_with_offset(to_element=bar_element, xoffset=30, yoffset=10).perform()
        # time.sleep(1)
        # ActionChains(self.browser).move_to_element_with_offset(to_element=bar_element, xoffset=100, yoffset=20).perform()
        # time.sleep(0.5)
        # ActionChains(self.browser).move_to_element_with_offset(to_element=bar_element, xoffset=200, yoffset=50).release().perform()
        # time.sleep(1.5)
        self.browser.get_screenshot_as_file('error.png')
        if self.__is_element_exist('.errloading > span'):
            error_message_element = self.browser.find_element_by_css_selector('.errloading > span')
            error_message = error_message_element.text
            self.browser.execute_script('noCaptcha.reset(1)')
            raise SessionException('滑动验证失败, message = ' + error_message)

    def __submit(self):
        """
        提交登录
        :return:
        """
        self.browser.find_element_by_id('J_SubmitStatic').click()
        time.sleep(0.5)
        if self.__is_element_exist("#J_Message"):
            error_message_element = self.browser.find_element_by_css_selector('#J_Message > p')
            error_message = error_message_element.text
            raise SessionException('登录出错, message = ' + error_message)

    def __navigate_to_target_pagevigate_to_target_page(self):
        self.browser.get('https://dushiliren.tmall.com/category-1444868252.htm?spm=a1z10.3-b-s.w4011-17964102365.2.5e3b7191N2PjGx&tsearch=y&orderType=hotsell_desc#TmshopSrchNav')
        time.sleep(10)
        self.html_source = self.browser.page_source
        soup = BeautifulSoup(self.html_source,'lxml')
        # print(soup)
        div = soup.find('div',class_='J_TItems')
        item4_list = div.find_all('div',class_="item4line1")
        for i in item4_list:
            dl_list = i.find_all('dl')
            for dl in dl_list:
                title = dl.find('dt',class_="photo").find('a').find('img')["alt"]
                img = dl.find('dt',class_="photo").find('a').find('img')["src"]
                price = dl.find('dd',class_="detail").find('span',class_="c-price")
                print(title,img,price)

        # with open('a.html','w',encoding='utf-8')as f:
        #     f.write(self.html_source)
        # print("写入成功")
    # 解析网页数据
    def __parse_page_content(self):
        time.sleep(20000)

    def __save_list_to_db(self, crawler_list):
        pass


    def __init_date(self):
        date_offset = 0
        self.today_date = (date.today() + timedelta(days=-date_offset)).strftime("%Y-%m-%d")
        self.yesterday_date = (date.today() + timedelta(days=-date_offset-1)).strftime("%Y-%m-%d")

    def __init_browser(self):
        """
        初始化selenium浏览器
        :return:
        """
        options = Options()
        # options.add_argument("--headless")
        prefs = {"profile.managed_default_content_settings.images": 1}
        options.add_experimental_option('excludeSwitches', ['enable-automation'])
        options.add_experimental_option("prefs", prefs)
        options.add_argument('--proxy-server=http://127.0.0.1:7878')
        options.add_argument('disable-infobars')
        options.add_argument('--no-sandbox')
        # options.add_argument('--user-data-dir=' + r'C:/Users/NALA/AppData/Local/Google/Chrome/User Data')


        self.browser = webdriver.Chrome(options=options)
        self.browser.implicitly_wait(3)
        self.browser.maximize_window()
        self.browser.get(TB_LOGIN_URL)

    def __is_element_exist(self, selector):
        """
        检查是否存在指定元素
        :param selector:
        :return:
        """
        try:
            self.browser.find_element_by_css_selector(selector)
            return True
        except NoSuchElementException:
            return False



#执行命令行
Crawler().start('1418768572x', '05710572x')
