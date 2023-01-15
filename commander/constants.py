import os
import platform

CWD = os.getcwd().replace('\\', '/')
CACHE_DIR = f"{CWD}/cache/"


PLATFORM = platform.system().lower()


OPTIONS = """
cp
mv
rm
""".strip()