# Make Youtube Speed Great Again!
# by nyako
# Inspired by this comment -- https://github.com/yt-dlp/yt-dlp/issues/10443#issuecomment-2248940967


import httpx
from io import BytesIO
import asyncio
import platform
import shutil
import zipfile



async def main():
    """
    This is some cringy code plz do not read.
    """
    # Okay, let's get actual version of byedpi
    res = httpx.get("https://api.github.com/repos/hufrea/byedpi/releases/latest").json()
    latest_tag = res['tag_name']

    os_type = platform.system()
    if os_type == "windows":
        archive = BytesIO(await httpx.get(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64-w64.zip").content)
        with zipfile.ZipFile(archive) as z:
            with z.open('/ciadpi.exe') as zf, open('./ciadpi.exe', 'wb') as f:
                shutil.copyfileobj(zf, f)
    elif os_type == "linux":
        archive = BytesIO(await httpx.get(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64.tar.gz").content)
        with zipfile.ZipFile(archive) as z:
            with z.open('/ciadpi') as zf, open('./ciadpi', 'wb') as f:
                shutil.copyfileobj(zf, f)
    

if __name__ == "__main__":
    asyncio.run(main())