import time
from selenium import webdriver
from main import API
api = API()


class Search(object):
    def __init__(self, message):
        self.__driver = webdriver.Chrome()
        self.__message = message
        self.__url = "https://www.baidu.com"
        self.__get_picture()

    def __get_picture(self):
        self.__driver.get(self.__url)
        input_box = self.__driver.find_element_by_class_name("s_ipt")
        input_box.send_keys(self.__message)
        input_box.submit()
        time.sleep(6)
        data = self.__driver.find_elements_by_xpath("//div[@id='content_left']//a")
        href_url = []
        for i in data:
            href_url.append(i.get_attribute("href"))
        self.__driver.switch_to.window(self.__driver.window_handles[0])
        self.__driver.get(href_url[0])
        api.send("搜索到:" + href_url[0])
        time.sleep(6)
        self.__driver.get_screenshot_as_file(f'{self.__message}.png')

    def __del__(self):
        self.__driver.close()
