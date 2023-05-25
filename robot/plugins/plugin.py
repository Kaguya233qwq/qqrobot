import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class GPT(object):
    def __init__(self, message):
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        self.message = message
        self.url = "https://gpt1.tool00.com/"
        self.driver = webdriver.Chrome(chrome_options=options)

    def __str__(self):
        self.driver.get(self.url)
        time.sleep(0.5)
        box = self.driver.find_element_by_xpath("//textarea[@id='chatgpt_input']")
        box.send_keys(self.message, Keys.ENTER)
        time.sleep(20)
        data = self.driver.find_elements_by_xpath("//tr[@class='bg-gray-50 bot']")
        data = str(data[1].text).split("\n")[1]
        return data

    def __del__(self):
        self.driver.close()
