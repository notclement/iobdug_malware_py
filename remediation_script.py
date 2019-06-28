import shutil
import os
from threading import Thread
try:
    import _winreg as winreg
except ImportError:
    # this has been renamed in python 3
    import winreg


def remove_folders_files():
    directory = "{}\\WinUpdate".format(os.getenv('LOCALAPPDATA'))
    try:
        shutil.rmtree(directory, ignore_errors=False, onerror=None)
    except:
        pass
    print "- All folder/file traces removed."


def remove_keys():
    # Computer\HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run
    # key: WinAutoUpdate
    key_path = r"Software\Microsoft\Windows\CurrentVersion\Run"
    value = 'WinAutoUpdate'
    key_HANDLE = winreg.OpenKey(winreg.HKEY_CURRENT_USER, key_path, 0, winreg.KEY_ALL_ACCESS)
    winreg.DeleteValue(key_HANDLE, value)
    print "- All related registry keys removed."


def main():
    Thread(target=remove_keys).start()
    Thread(target=remove_folders_files()).start()
    print "You're all cleaned up!"


if __name__ == '__main__':
    main()
