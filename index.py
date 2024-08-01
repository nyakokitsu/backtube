# Make Youtube Speed Great Again!
# by nyako
# Inspired by this comment -- https://github.com/yt-dlp/yt-dlp/issues/10443#issuecomment-2248940967


import requests
import asyncio
import platform
import shutil
import zipfile
import tarfile
import os
import pathlib
import sys

user_dir = pathlib.Path.home() / "AppData" / "Roaming" / "Microsoft" / "Windows" / "Start Menu" / "Programs" / "Startup" 

async def main():
    """
    This is some cringy code plz do not read.
    """
    

    # Okay, let's get actual version of byedpi
    res = requests.get("https://api.github.com/repos/hufrea/byedpi/releases/latest").json()
    latest_tag = res['tag_name']
    

    os_type = platform.system()
    print("nyako's byeDPI installer")
    print("MAKE YOUTUBE GREAT AGAIN!\n")

    is_installed = check_installed(os_type)

    if is_installed:
        uninstall_ask = ask("Found installation, start uninstall?")
        if uninstall_ask:
            os.remove("%appdata%\Roaming\byeDPI\ciadpi.exe")
            if (user_dir / "dpi.bat").exists():
                os.remove(user_dir / "dpi.bat")
            print("Uninstallation complete!")
            input("Press Enter to exit.")
                

    print(f"Latest version of byeDPI: {latest_tag}\n")
    print(f"Platform: {os_type}")
    if os_type == "Windows":
        fetch_file(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64-w64.zip", True)
        with zipfile.ZipFile("byedpi.zip", 'r') as z:
            with z.open('ciadpi.exe') as zf, open('./ciadpi.exe', 'wb') as f:
                shutil.copyfileobj(zf, f)
        if os.path.exists("byedpi.zip"):
            os.remove("byedpi.zip")
    elif os_type == "Linux":
        fetch_file(f"https://github.com/hufrea/byedpi/releases/download/{latest_tag}/byedpi-12-x86_64.tar.gz", False)
        with tarfile.open("byedpi.tar.gz", 'r:gz') as tar:
            tar.extract('ciadpi-x86_64')
        if os.path.exists("byedpi.tar.gz"):
            os.remove("byedpi.tar.gz")
        if os.path.exists('ciadpi-x86_64'):
            os.rename('ciadpi-x86_64', 'ciadpi')
    print("File extracted!")
    print("Setting some variables...")
    # Set startup.
    if os_type == "Windows":
        win_strategy()
    elif os_type == "Linux":
        linux_strategy()

def linux_strategy():
    print("Service configuration not realized =( \ntodo ;)\nyou can run exec in screen")

def win_move():
    user_dir = pathlib.Path.home() / "AppData" / "Roaming" / "byeDPI"
    if not user_dir.exists():
        os.mkdir(user_dir)
        shutil.copyfile("ciadpi.exe", pathlib.Path.home() / "AppData" / "Roaming" / "byeDPI" / "ciadpi.exe")

def win_strategy():
    need_autostart = ask("Needed to add to autostart?")
    cia_path = pathlib.Path.home() / "AppData" / "Roaming" / "byeDPI"
    if need_autostart:
        with open(user_dir / "dpi.bat", "w") as bat_file:
            bat_file.write(f"cd {cia_path} && ciadpi.exe -i 127.0.0.1 -p 10801 -d 1")
    os.system("netsh winhttp set proxy socks5://127.0.0.1:10801")
    print('Successfully added proxy! Running ciadpi...')
    os.system(f"cd {cia_path} && ciadpi.exe -i 127.0.0.1 -p 10801 -d 1")



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




def ask(question, default="yes"):
    valid = {"yes": True, "y": True, "ye": True, "no": False, "n": False}
    if default is None:
        prompt = " [y/n] "
    elif default == "yes":
        prompt = " [Y/n] "
    elif default == "no":
        prompt = " [y/N] "
    else:
        raise ValueError("invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = input().lower()
        if default is not None and choice == "":
            return valid[default]
        elif choice in valid:
            return valid[choice]
        else:
            sys.stdout.write("Please respond with 'yes' or 'no' " "(or 'y' or 'n').\n")

def check_installed(os_type):
    if os_type == "Windows":
        cia_path = pathlib.Path.home() / "AppData" / "Roaming" / "byeDPI" / "ciadpi.exe"
        if cia_path.exists():
            return True
        else:
            return False
    else:
        print("Not found any configuration.")
        return False



if __name__ == "__main__":
    asyncio.run(main())
