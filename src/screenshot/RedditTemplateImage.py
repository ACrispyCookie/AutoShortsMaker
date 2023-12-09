import random

from PIL import ImageDraw, ImageFont
from PIL import Image

post_template = "templates/reddit_ask/template-post"
comment_template = "templates/reddit_ask/template-comment"
comment_timestamp = "templates/reddit_ask/timestamp-comment.png"
random_names = "templates/reddit_ask/usernames.txt"
font_path = "templates/reddit_ask/NotoSans-Regular.ttf"
font_path_bold = "templates/reddit_ask/NotoSans-Bold.ttf"
max_line_length = 483 - 60  # 483 is the width of the template image, 60 is the margin size

post_pos = {"username": (56, 42), "body": (16, 66)}
post_properties = {"username": {"size": 12, "fill": (184, 197, 201), "path": font_path},
                   "body": {"size": 17, "fill": (242, 242, 242), "path": font_path_bold}}
comment_pos = {"username": (50, 20), "body": (50, 51)}
comment_properties = {"username": {"size": 11, "fill": (242, 242, 242), "path": font_path_bold},
                      "body": {"size": 12, "fill": (242, 242, 242), "path": font_path}}


class RedditTemplateImage:

    def __init__(self, content):
        self.content = content
        self.used_names = []
        self.create()

    def create(self):
        template = post_template if self.content.type == 'post' else comment_template
        properties = post_properties if self.content.type == 'post' else comment_properties
        pos = post_pos if self.content.type == 'post' else comment_pos
        timestamp = None if self.content.type == 'post' else comment_timestamp
        lines = splitText(self.content.body, properties)

        header = Image.open(template + "-header.png").convert("RGBA")
        line = Image.open(template + "-line.png").convert("RGBA")
        footer = Image.open(template + "-footer.png").convert("RGBA")
        height = len(lines) * (34 if self.content.type == 'post' else 24) + 56 if self.content.type == 'post' else 65

        username = self.getRandomUsername()
        image = Image.new("RGB", (483, height), (0, 0, 0))
        image.paste(header, (0, 0), header)
        draw = ImageDraw.Draw(image)

        # Draw username
        font = ImageFont.truetype(properties["username"]["path"], properties["username"]["size"])
        length = draw.textlength(username, font=font)
        draw.text(pos["username"], username, font=font, fill=properties["username"]["fill"])

        # Draw timestamp
        if self.content.type == 'comment':
            timestamp_image = Image.open(timestamp).convert("RGBA")
            image.paste(timestamp_image, (int(pos["username"][0] + length + 5), int(pos["username"][1]) + 2),
                        timestamp_image)

        # Draw body
        font = ImageFont.truetype(properties["body"]["path"], properties["body"]["size"])
        for i in range(len(lines)):
            draw.text((pos["body"][0], pos["body"][1] + i * 34), lines[i], font=font, fill=properties["body"]["fill"])
            image.paste(line, (0, 34 + i * 34), line)

        # Draw footer
        image.paste(footer, (0, len(lines) * 34), footer)

        image.save(self.content.screenshot)

    def getRandomUsername(self):
        with open(random_names) as f:
            lines = f.readlines()
            line = random.choice(lines)
            while line in self.used_names:
                line = random.choice(lines)
            self.used_names.append(line)
            return line.strip()


def splitText(text, properties):
    image = Image.open(post_template + "-header.png").convert("RGBA")
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(properties["username"]["path"], properties["username"]["size"])

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

    return lines
