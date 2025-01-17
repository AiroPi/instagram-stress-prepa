import asyncio
import os
from pathlib import Path

from aiograpi import Client
from schedule import (
    every,
    repeat,
    run_pending,
)

from image import make_image

try:
    from dotenv import load_dotenv  # pyright: ignore[reportMissingImports]
except ModuleNotFoundError:
    pass
else:
    load_dotenv()

DATA_DIR = Path("./data/")
SESSION_PATH = DATA_DIR / "session.json"

USERNAME = os.environ["USERNAME"]
PASSWORD = os.environ["PASSWORD"]

TASKS = []


async def get_client(force_reconnect: bool = False):
    cl = Client()

    if SESSION_PATH.exists() and not force_reconnect:
        cl.load_settings(SESSION_PATH)

    await cl.login(os.environ["USERNAME"], os.environ["PASSWORD"])

    cl.dump_settings(SESSION_PATH)

    return cl


@repeat(every().day.at("07:00", "Europe/Paris"))
def post():
    print("Posting a new image...")
    task = asyncio.create_task(_post())
    TASKS.append(task)  # keep a reference
    task.add_done_callback(lambda t: TASKS.remove(t))


async def _post():
    image = make_image()
    image.convert("RGB").save("./tmp.jpg", "JPEG")

    client = await get_client()
    try:
        await client.photo_upload(Path("./tmp.jpg"), "Courage!")
    except Exception as e:
        print("Failed !")
        print(e)
    else:
        print("New image posted !")


async def main():
    while True:
        run_pending()
        await asyncio.sleep(1)


if __name__ == "__main__":
    print("Up!")
    if not DATA_DIR.exists():
        DATA_DIR.mkdir()

    asyncio.run(main())
