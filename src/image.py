import datetime as dt
from zoneinfo import ZoneInfo

from PIL import Image, ImageDraw, ImageFont

from utils import all_units, progress

BACKGROUND = Image.open("./resources/images/background.png")
PROGRESS_BAR = Image.open("./resources/images/progress-bar.png")
SIZE = (2000, 2000)

FONT_PATH = "./resources/fonts/Chalkduster.ttf"

BACK_TO_SCHOOL = dt.datetime(2024, 9, 2, 8, tzinfo=ZoneInfo("Europe/Paris"))
XENS = dt.datetime(2025, 4, 14, 8, tzinfo=ZoneInfo("Europe/Paris"))


def make_image():
    now = dt.datetime.now(tz=ZoneInfo("Europe/Paris"))
    percent = progress(BACK_TO_SCHOOL, now, XENS)
    months, days = all_units(XENS - now)

    mask = Image.new("L", SIZE, 0)
    progress_bar_mask = Image.new("L", SIZE, 0)
    draw = ImageDraw.Draw(mask)
    # The progress bar is 1750px wide and centered. The mask will mask pixels on the right of the progress bar.
    draw.rectangle((0, 0, 125 + percent * 1750, 2000), 255)
    # Set the shape of the progress bar, so only those pixels will be "printed" on the background.
    progress_bar_mask.paste(mask, (0, 0), PROGRESS_BAR)

    result = BACKGROUND.copy()
    result.paste(PROGRESS_BAR, mask=progress_bar_mask)
    draw = ImageDraw.Draw(result)

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
        # Please, don't do that. It's just because it's new in 3.12 :)
        f"Plus que {f'{months} mois et ' if months else ''}{days} jour(s)",
        font=font,
        fill=(255, 255, 255),
        anchor="mm",
    )

    return result
