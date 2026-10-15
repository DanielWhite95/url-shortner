import asyncio
from url_shortner.main import main as app_main

def main() -> None:
    asyncio.run(app_main())
