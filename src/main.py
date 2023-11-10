import datetime as dt
import os
import time
from zoneinfo import ZoneInfo

from instauto.api.client import ApiClient
from instauto.helpers.post import upload_image_to_feed
from PIL import Image, ImageDraw, ImageFont
from schedule import repeat  # pyright: ignore[reportUnknownVariableType]
from schedule import every, run_pending

try:
    from dotenv import load_dotenv
except ModuleNotFoundError:
    pass
else:
    load_dotenv()


BACKGROUND = Image.open("./resources/images/background.png")
PROGRESS_BAR = Image.open("./resources/images/progress-bar.png")
SIZE = (2000, 2000)

FONT_PATH = "./resources/fonts/Chalkduster.ttf"
SESSION_PATH = "./data/session.instauto"

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

BACK_TO_SCHOOL = dt.datetime(2023, 9, 4, 8, tzinfo=ZoneInfo("Europe/Paris"))
XENS = dt.datetime(2024, 4, 15, 8, tzinfo=ZoneInfo("Europe/Paris"))

mask = Image.new("L", SIZE, 0)
progress_bar_mask = Image.new("L", SIZE, 0)

if not os.path.exists(SESSION_PATH):
    client = ApiClient(username=USERNAME, password=PASSWORD)
    client.log_in()
    client.save_to_disk(SESSION_PATH)
else:
    client = ApiClient.initiate_from_file(SESSION_PATH)


def make_image():
    now = dt.datetime.now(tz=ZoneInfo("Europe/Paris"))
    percent = progress(BACK_TO_SCHOOL, now, XENS)
    months, days = all_units(XENS - now)

    background = BACKGROUND.copy()

    draw = ImageDraw.Draw(mask)
    draw.rectangle((0, 0, 125 + percent * 1750, 2000), 255)

    # set the shape of the progress bar
    progress_bar_mask.paste(mask, (0, 0), PROGRESS_BAR)

    background.paste(PROGRESS_BAR, (0, 0), progress_bar_mask)

    draw = ImageDraw.Draw(background)

    font = ImageFont.truetype(FONT_PATH, 100)
    draw.text(  # pyright: ignore[reportUnknownMemberType]
        (2000 - 125, 1100),
        f"{percent * 100:.0f}%",
        font=font,
        fill=(255, 255, 255),
        anchor="rt",
    )

    draw.text(  # pyright: ignore[reportUnknownMemberType]
        (1000, 1500),
        f"Plus que {f"{months} mois et " if months else ""}{days} jour(s)",
        font=font,
        fill=(255, 255, 255),
        anchor="mm",
    )

    return background


def all_units(delta: dt.timedelta):
    """
    Split a timedelta into units if time.

    Returns:
        A tuple with the following units: (months, days)
    """
    seconds = delta.total_seconds()
    months, rest = divmod(seconds, 3600 * 24 * 30.5)
    # weeks, rest = divmod(rest, 3600 * 24 * 7)
    days, rest = divmod(rest, 3600 * 24)
    # hours, rest = divmod(rest, 3600)
    # minutes, rest = divmod(rest, 60)
    # seconds = rest

    # return tuple(int(v) for v in (months, weeks, days, hours, minutes, seconds))
    return tuple(int(v) for v in (months, days))


def progress(start: dt.datetime, current: dt.datetime, end: dt.datetime):
    """
    Returns:
        A float between 0 and 1, representing the progress of the current datetime between the start and end datetimes.
    """
    total = (end - start).total_seconds()
    state = (current - start).total_seconds()
    return state / total


@repeat(every().day.at("07:00", "Europe/Paris"))
def post():
    image = make_image()
    image.save("./tmp.jpg", "JPEG")
    upload_image_to_feed(client, "./tmp.jpg", "Courage!")

make_image().convert("RGB").save("./tmp.jpg", "JPEG")

if __name__ == "__main__":
    while True:
        run_pending()
        time.sleep(1)
