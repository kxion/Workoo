'''
Empty
'''
import re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, StaleElementReferenceException, TimeoutException
from utils.request import Query
from utils.soup import DealSoup


def remove_charater(content: str):
    return content.replace('\n', '').replace('\t',
                                             '').replace('\r',
                                                         '').replace(' ', '')


class OperaChrome(object):
    def __init__(self, path=None):
        self.init_chrome(path)

    def get_proxy(self):
        req = Query().run
        resp = req(
            path=
            'http://route.xiongmaodaili.com/xiongmao-web/api/glip?secret=3648c286d4be950dfeb744412178bab8&orderNo=GL20191218133200tOpTjxj6&count=1&isTxt=1&proxyType=1'
        )
        return remove_charater(resp)

    def init_chrome(self, path):
        options = webdriver.ChromeOptions()
        options.add_argument("disable-infobars")
        options.add_argument("disable-web-security")
        # options.add_argument("--headless")
        options.add_argument("--start-maximized")
        options.add_argument('--log-level=3')
        options.add_argument('--ignore-certificate-errors')
        options.add_experimental_option('excludeSwitches',
                                        ['enable-automation'])

        # options.add_argument('--proxy-server=http://{}'.format(
        #     self.get_proxy()))

        # prefs = {"profile.managed_default_content_settings.images": 2}
        # options.add_experimental_option("prefs", prefs)
        driver = webdriver.Chrome(executable_path="./chromedriver.exe",
                                  options=options)
        if path is not None:
            driver.get(path)

        self.driver = driver

    def judge_driver(self, driver):
        if driver is None:
            return self.driver
        else:
            return driver

    def waiting(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        while True:
            try:
                WebDriverWait(driver, timeout, 0.1).until(
                    EC.presence_of_element_located((By.XPATH, xpath)))
            except IndexError as exc:
                print("---> Waiting for tm-indcon")
                continue
            except StaleElementReferenceException as exc:
                print("---> Waiting for count monthly")
                continue
            except TimeoutException:
                print('timeout')
                return False
            else:

                return True

    def click(self, xpath, driver=None, timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).click()

    def input(self, xpath, driver=None, keyword='', timeout=15):
        driver = self.judge_driver(driver)

        if self.waiting(xpath, timeout=timeout):
            driver.find_element_by_xpath(xpath).send_keys(keyword)


class Amazon(object):
    def __init__(self):
        super().__init__()

    def starts_parser(self, html):
        pref_list = []
        soup = DealSoup()
        cards = soup.judge(
            html,
            attr={
                'class': ['a-section sp_offerVertical p13n-asin sp_ltr_offer']
            },
            all_tag=True)
        # cards = soup.judge(html, attr={'id': 'a-carousel'})
        for card in cards:
            pref = card['data-viewpixelurl']
            pref_list.append('https://www.amazon.com{}'.format(pref))

        # //*[@id="a-autoid-19"]

    def parser(self):
        html = self.chrome.driver.page_source

        info = {}
        soup = DealSoup()

        info['品牌'] = soup.judge(html, attr={'id': 'bylineInfo'}).text
        temp = soup.judge(html, attr={'id': 'averageCustomerReviews'})
        info['星级'] = soup.judge(temp, attr={'class': 'a-icon-alt'}).text
        info['评价'] = soup.judge(temp, attr={
            'id': 'acrCustomerReviewText'
        }).text
        info['价格'] = soup.judge(html, attr={'id': 'priceblock_ourprice'}).text

        result = re.search(r'"dimensionToAsinMap" : (\{.*\})', html)
        if result:
            data = result.group(1)
            info['变体数量'] = len(data)
            info['变体'] = data

        # for class_name in []:

        # 4 stars and aboveq
        starts = soup.judge(html, attr={'class': 'a-carousel-row-inner'})
        if starts:
            self.starts_parser(starts)

        print(info)

    def main(self):
        path = 'https://www.amazon.com/dp/B073FLCFK2?th=1&psc=1'
        self.chrome = OperaChrome(path)
        timeout = 15
        self.chrome.click('//*[@id="nav-global-location-slot"]/span/a',
                          timeout=timeout)
        self.chrome.input('//*[@id="GLUXZipUpdateInput"]',
                          keyword='90005',
                          timeout=timeout)
        self.chrome.click('//*[@id="GLUXZipUpdate"]/span/input',
                          timeout=timeout)
        self.chrome.click(
            '//*[@id="a-popover-8"]/div/div[2]/span/span/span/button',
            timeout=timeout)
        # chrome.click('//*[@id="GLUXConfirmClose"]', timeout=timeout)
        self.chrome.click('//*[@id="a-popover-7"]/div/div[2]/span/span',
                          timeout=timeout)

        self.chrome.driver.find_element_by_xpath()
        self.parser()


if __name__ == "__main__":
    spider = Amazon()
    spider.main()