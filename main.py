from Scripts.modules import first_start_check,cls
import ctypes
def is_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return "У скрипта нет административных прав для запуска"
is_admin()
cls()
first_start_check()