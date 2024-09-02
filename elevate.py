import sys
import ctypes
import win32com.shell.shell as shell
ASADMIN = 'asadmin'

def elevate():
    if sys.argv[-1] != ASADMIN:
        script = sys.executable
        params = ' '.join([script] + sys.argv[1:] + [ASADMIN])
        shell.ShellExecuteEx(lpVerb='runas', lpFile=sys.executable, lpParameters=params)
        sys.exit(0)

if __name__ == '__main__':
    elevate()