import os

CWD = os.getcwd().replace('\\', '/')
CACHE_DIR = f"{CWD}/cache/"



OPTIONS = """
cp
mv
rm
""".strip()