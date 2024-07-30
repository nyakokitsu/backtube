# Make Youtube Speed Great Again!
# by nyako
# Inspired by this comment -- https://github.com/yt-dlp/yt-dlp/issues/10443#issuecomment-2248940967


import requests
import httpx
import asyncio
import platform
import shutil
import zipfile
import tarfile
import os

async def main():
    """
    This is some cringy code plz do not read.
    """
    # Okay, let's get actual version of byedpi
    res = httpx.get("https://api.github.com/repos/hufrea/byedpi/releases/latest").json()
    latest_tag = res['tag_name']

    os_type = platform.system()
    print("nyako's byeDPI installer")
    print("MAKE YOUTUBE GREAT AGAIN!")
    print(f"Latest version of byeDPI: {latest_tag}")
    print(f"Platform: {os_type}")
    if os_type == "Windows":
        fetch_file(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64-w64.zip", True)
        with zipfile.ZipFile("byedpi.zip") as z:
            with z.open('ciadpi.exe') as zf, open('./ciadpi.exe', 'wb') as f:
                shutil.copyfileobj(zf, f)
        z.close()
        os.remove("byedpi.zip")
    elif os_type == "Linux":
        fetch_file(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64.tar.gz", False)
        tar = tarfile.open("byedpi.tar.gz")
        tar.extract('ciadpi-x86_64')
        tar.close()
        os.remove("byedpi.tar.gz")
        os.rename('ciadpi-x86_64', 'ciadpi')
    print("File extracted!")
    
def fetch_file(URL: str, is_win: bool):
    try:
        response = requests.get(URL)
    except OSError:
        print('No connection to the server!')
        return None

    # check if the request is succesful
    if response.status_code == 200:
        # Save dataset to file
        print('File downloaded!')
        open('byedpi.zip' if is_win else 'byedpi.tar.gz', 'wb').write(response.content)
    else:
        print('File request not successful!.')
        return None

if __name__ == "__main__":
    asyncio.run(main())