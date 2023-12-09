import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

screenWidth = 400
screenHeight = 800


class RedditScreenshot:

    def __init__(self, post, comments):
        self.post = post
        self.comments = comments
        print("Comments: " + str(len(comments)))
        for comment in comments:
            print(comment.id)
        self.driver, self.wait = self.setupDriver()
        if self.post is not None:
            self.screenshotPost()
        if self.comments is not None:
            self.screenshotComments()
        self.driver.quit()

    def screenshotPost(self):
        search = self.wait.until(EC.presence_of_element_located((By.TAG_NAME, "shreddit-post")))
        self.driver.execute_script("window.focus();")

        file_name = f"screenshots/reddit_ask/post-{self.post.id}.png"
        fp = open(file_name, "wb")
        fp.write(search.screenshot_as_png)
        fp.close()

    def screenshotComments(self):
        for comment in self.comments:
            search = self.wait.until(
                EC.presence_of_element_located((By.XPATH, f'//shreddit-comment[@thingid="t1_{comment.id}"]')))
            self.driver.execute_script("window.focus();")

            file_name = f"screenshots/reddit_ask/comment-{comment.id}.png"
            fp = open(file_name, "wb")
            fp.write(search.screenshot_as_png)
            fp.close()

    def setupDriver(self):
        options = webdriver.ChromeOptions()
        options.headless = False
        proxy_server = "103.21.244.18:80"
        #options.add_argument(f'--proxy-server={proxy_server}')
        driver = webdriver.Chrome(options=options)
        wait = WebDriverWait(driver, 10)

        driver.set_window_size(width=screenWidth, height=screenHeight)
        driver.get(self.post.url)

        return driver, wait
