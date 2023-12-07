import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

screenWidth = 400
screenHeight = 800


class RedditScreenshot:

    def __init__(self, url, post_id=None, comments=None):
        self.url = url
        self.post_id = post_id
        self.comments = comments
        self.driver, self.wait = self.setupDriver()
        if self.post_id is not None:
            self.screenshotPost()
        if self.comments is not None:
            self.screenshotComments()
        self.driver.quit()

    def screenshotPost(self):
        search = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-post")))
        self.driver.execute_script("window.focus();")

        file_name = f"screenshots/reddit_ask/post-{self.post_id}.png"
        fp = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def screenshotComments(self):
        for comment in self.comments:
            search = self.wait.until(EC.presence_of_element_located((By.XPATH, f'//shreddit-comment[@thingid="t1_{comment.id}"]')))
            self.driver.execute_script("window.focus();")

            file_name = f"screenshots/reddit_ask/comment-{comment.id}.png"
            fp = open(file_name, "wb")
            fp.write(search.screenshot_as_png)
            fp.close()

    def setupDriver(self):
        options = webdriver.ChromeOptions()
        options.headless = False
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        driver.set_window_size(width=screenWidth, height=screenHeight)
        driver.get(self.url)

        return driver, wait
