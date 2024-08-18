import random
from typing import Tuple, Dict, Any, List

from PIL import ImageDraw, ImageFont
from PIL import Image
from PIL.ImageFont import FreeTypeFont

from content.types.reddit_ask.images.RedditImage import RedditImage

post_template: str = "data/reddit_ask/templates/template-post"
comment_template: str = "data/reddit_ask/templates/template-comment"
comment_timestamp: str = "data/reddit_ask/templates/template-comment-timestamp.png"
random_names: str = "data/reddit_ask/templates/usernames.txt"
font_path: str = "data/reddit_ask/templates/NotoSans-Regular.ttf"
font_path_bold: str = "data/reddit_ask/templates/NotoSans-Bold.ttf"
# TODO Deal with static dirs

post_pos: Dict[str, Tuple[int, int]] = {"username": (92, 35), "body": (31, 64)}
post_properties: Dict[str, Any] = {"username": {"size": 14, "fill": (184, 197, 201), "path": font_path},
                   "body": {"size": 28, "fill": (242, 242, 242), "path": font_path_bold}}
comment_pos: Dict[str, Tuple[int, int]] = {"username": (70, 25), "body": (68, 60)}
comment_properties: Dict[str, Any] = {"username": {"size": 13, "fill": (242, 242, 242), "path": font_path_bold},
                      "body": {"size": 16, "fill": (242, 242, 242), "path": font_path}}

width: int = 300
post_height: Dict[str, int] = {"header": 68, "footer": 100, "line": 43}
comment_height: Dict[str, int] = {"header": 59, "footer": 90, "line": 25}


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
        max_line_length: int = width - self.pos["body"][0] - 25
        lines: List[str] = split_text(self.content.body, ImageFont.truetype(self.properties["body"]["path"],
                                                                 self.properties["body"]["size"]), max_line_length)

        header: Image = Image.open(self.template + "-header.png").convert("RGBA")
        line: Image = Image.open(self.template + "-line.png").convert("RGBA")
        footer: Image = Image.open(self.template + "-footer.png").convert("RGBA")

        header_height: int = self.height["header"]
        body_height: int = len(lines) * self.height["line"]
        footer_height: int = 0  # self.height["footer"]

        draw, image, font, length = self.draw_username(header_height + body_height + footer_height, header,
                                                       self.properties, self.pos)

        # Draw timestamp
        if self.content.type == 'comment':
            timestamp_image: Image = Image.open(self.timestamp).convert("RGBA")
            image.paste(timestamp_image, (int(self.pos["username"][0] + length + 4), int(self.pos["username"][1]) + 4),
                        timestamp_image)

        self.draw_body(image, self.pos, header_height, line, lines, self.properties)

        # Draw footer
        # image.paste(footer, (0, header_height + body_height), footer)

        image.save(self.content.image)

    def get_random_username(self):
        with open(random_names) as f:
            lines = f.readlines()
            line = random.choice(lines)
            while line in self.used_names:
                line = random.choice(lines)
            self.used_names.append(line)
            return line.strip()

    def draw_username(self, total_height: int, header: Image, properties: Dict[str, Any], pos: Dict[str, Tuple[int, int]]) -> Tuple[ImageDraw, Image, FreeTypeFont, float]:
        image: Image = Image.new("RGB", (width, total_height), (0, 0, 0))
        image.paste(header, (0, 0), header)
        draw: ImageDraw = ImageDraw.Draw(image)

        # Draw username
        font: FreeTypeFont = ImageFont.truetype(properties["username"]["path"], properties["username"]["size"])
        length: float = draw.textlength(self.content.author, font=font)
        draw.text(pos["username"], self.content.author, font=font, fill=properties["username"]["fill"])

        return draw, image, font, length

    def draw_body(self, image: Image, pos: Dict[str, Tuple[int, int]], header_height: int, line: Image, lines: List[str], properties: Dict[str, Any]):
        draw: ImageDraw = ImageDraw.Draw(image)

        # Draw body
        font: FreeTypeFont = ImageFont.truetype(properties["body"]["path"], properties["body"]["size"])
        for i in range(len(lines)):
            image.paste(line, (0, header_height + i * self.height["line"]), line)
            draw.text((pos["body"][0], pos["body"][1] + i * self.height["line"]), lines[i], font=font,
                      fill=properties["body"]["fill"])


def split_text(text: str, font, max_line_length: int) -> List[str]:
    image: Image = Image.open(post_template + "-line.png").convert("RGBA")
    draw: ImageDraw = ImageDraw.Draw(image)
    text: str = text.replace("\n", " ")

    lines: List[str] = []
    line: str = ""
    line_length: int = 0

    words: List[str] = text.split(" ")
    for word in words:
        word_length: float = draw.textlength(word, font=font)
        if word_length + line_length > max_line_length:
            lines.append(line)
            line = ""
            line_length = 0
        line += word + " "
        line_length += word_length

    lines.append(line)
    return lines
