from typing import Tuple, BinaryIO

import selenium.webdriver as webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from content.types.reddit_ask.images.RedditImage import RedditImage

screenWidth = 400
screenHeight = 800


class RedditScreenshot(RedditImage):

    def __init__(self, reddit_content):
        super().__init__(reddit_content)
        self.driver, self.wait = self.setup_driver()

    def create(self):
        if self.content.type == "post":
            self.screenshot_post()
        else:
            self.screenshot_comment()
        self.driver.quit()

    def screenshot_post(self):
        search = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-post")))
        self.driver.execute_script("window.focus();")

        file_name: str = self.content.image
        fp: BinaryIO = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def screenshot_comment(self):
        search = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//shreddit-comment[@thingid="t1_{self.content.id}"]')))
        self.driver.execute_script("window.focus();")

        file_name: str = self.content.image
        fp: BinaryIO = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def setup_driver(self) -> Tuple[WebDriver, WebDriverWait]:
        options: Options = webdriver.ChromeOptions()
        options.headless = False
        driver: WebDriver = webdriver.Chrome(options=options)
        wait: WebDriverWait = WebDriverWait(driver, 10)

        driver.set_window_size(width=screenWidth, height=screenHeight)
        driver.get(self.content.url)

        return driver, wait
