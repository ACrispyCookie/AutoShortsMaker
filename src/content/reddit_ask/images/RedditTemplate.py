import random

from PIL import ImageDraw, ImageFont
from PIL import Image

from src.content.reddit_ask.images.RedditImage import RedditImage

post_template = "data/reddit_ask/templates/template-post"
comment_template = "data/reddit_ask/templates/template-comment"
comment_timestamp = "data/reddit_ask/templates/template-comment-timestamp.png"
random_names = "data/reddit_ask/templates/usernames.txt"
font_path = "data/reddit_ask/templates/NotoSans-Regular.ttf"
font_path_bold = "data/reddit_ask/templates/NotoSans-Bold.ttf"
# TODO Deal with static dirs

post_pos = {"username": (67, 35), "body": (7, 64)}
post_properties = {"username": {"size": 14, "fill": (184, 197, 201), "path": font_path},
                   "body": {"size": 28, "fill": (242, 242, 242), "path": font_path_bold}}
comment_pos = {"username": (70, 25), "body": (68, 60)}
comment_properties = {"username": {"size": 13, "fill": (242, 242, 242), "path": font_path_bold},
                      "body": {"size": 14, "fill": (242, 242, 242), "path": font_path}}

width = 900
post_height = {"header": 68, "footer": 68, "line": 43}
comment_height = {"header": 59, "footer": 90, "line": 25}
max_line_length = width - 60  # 60 is the margin size


class RedditTemplate(RedditImage):

    def __init__(self, content):
        super().__init__(content)
        self.used_names = []
        self.template, self.properties, self.pos, self.timestamp, self.height = (
            post_template if self.content.type == "post" else comment_template,
            post_properties if self.content.type == "post" else comment_properties,
            post_pos if self.content.type == "post" else comment_pos,
            None if self.content.type == "post" else comment_timestamp,
            post_height if self.content.type == "post" else comment_height)

    def create(self):
        lines = splitText(self.content.body, self.properties)

        header = Image.open(self.template + "-header.png").convert("RGBA")
        line = Image.open(self.template + "-line.png").convert("RGBA")
        footer = Image.open(self.template + "-footer.png").convert("RGBA")

        header_height = self.height["header"]
        body_height = len(lines) * self.height["line"]
        footer_height = self.height["footer"]

        draw, image, font, length = self.drawUsername(header_height + body_height + footer_height, header,
                                                      self.properties, self.pos)

        # Draw timestamp
        if self.content.type == 'comment':
            timestamp_image = Image.open(self.timestamp).convert("RGBA")
            image.paste(timestamp_image, (int(self.pos["username"][0] + length + 4), int(self.pos["username"][1]) + 4),
                        timestamp_image)

        self.drawBody(image, self.pos, header_height, line, lines, self.properties)

        # Draw extra lines on post types
        if self.content.type == 'post':
            image.paste(line, (0, header_height + len(lines) * post_height["line"]), line)

        # Draw footer
        image.paste(footer, (0, header_height + body_height), footer)

        image.save(self.content.image)

    def getRandomUsername(self):
        with open(random_names) as f:
            lines = f.readlines()
            line = random.choice(lines)
            while line in self.used_names:
                line = random.choice(lines)
            self.used_names.append(line)
            return line.strip()

    def drawUsername(self, total_height, header, properties, pos):
        image = Image.new("RGB", (width, total_height), (0, 0, 0))
        image.paste(header, (0, 0), header)
        draw = ImageDraw.Draw(image)

        # Draw username
        font = ImageFont.truetype(properties["username"]["path"], properties["username"]["size"])
        length = draw.textlength(self.content.author, font=font)
        draw.text(pos["username"], self.content.author, font=font, fill=properties["username"]["fill"])

        return draw, image, font, length

    def drawBody(self, image, pos, header_height, line, lines, properties):
        draw = ImageDraw.Draw(image)

        # Draw body
        font = ImageFont.truetype(properties["body"]["path"], properties["body"]["size"])
        for i in range(len(lines)):
            height_per_line = post_height["line"] if self.content.type == 'post' else comment_height["line"]
            image.paste(line, (0, header_height + i * height_per_line), line)
            draw.text((pos["body"][0], pos["body"][1] + i * height_per_line), lines[i], font=font,
                      fill=properties["body"]["fill"])


def splitText(text, properties):
    image = Image.open(post_template + "-line.png").convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(properties["username"]["path"], properties["username"]["size"])
    text = text.replace("\n", " ")

    lines = []
    line = ""
    line_length = 0

    words = text.split(" ")
    for word in words:
        word_length = draw.textlength(word, font=font)
        if word_length + line_length > max_line_length:
            lines.append(line)
            line = ""
        line += word + " "
        line_length += word_length

    lines.append(line)
    return lines
