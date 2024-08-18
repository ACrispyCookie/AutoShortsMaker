import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

from content.types.reddit_ask.images.RedditImage import RedditImage

screenWidth = 400
screenHeight = 800


class RedditScreenshot(RedditImage):

    def __init__(self, reddit_content):
        super().__init__(reddit_content)
        self.driver, self.wait = self.setupDriver()

    def create(self):
        if self.content.type == "post":
            self.screenshotPost()
        else:
            self.screenshotComment()
        self.driver.quit()

    def screenshotPost(self):
        search = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-post")))
        self.driver.execute_script("window.focus();")

        file_name = self.content.image
        fp = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def screenshotComment(self):
        search = self.wait.until(
            EC.presence_of_element_located((By.XPATH, f'//shreddit-comment[@thingid="t1_{self.content.id}"]')))
        self.driver.execute_script("window.focus();")

        file_name = self.content.image
        fp = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def setupDriver(self):
        options = webdriver.ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        driver.set_window_size(width=screenWidth, height=screenHeight)
        driver.get(self.content.url)

        return driver, wait
