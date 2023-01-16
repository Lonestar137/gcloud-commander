import os
import platform

CWD = os.getcwd().replace('\\', '/')
CACHE_DIR = f"{CWD}/cache/"


PLATFORM = platform.system().lower()


OPTIONS = """
ls
cp
mv
rm
""".strip()