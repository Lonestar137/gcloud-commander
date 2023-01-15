import subprocess
import os
from logger import *
from argparse import ArgumentParser
from walker.datacache import cache_data, load_cache_data

def localdir(args, base_path_to_fzf)->str:
    result = ""
    base_path_to_fzf = base_path_to_fzf.replace('\n', '')
    fzf = subprocess.Popen(["fzf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    for dirpath, dirnames, filenames in os.walk(base_path_to_fzf):
        dirpath = dirpath.replace('\\', '/')
        for filename in filenames:
            line = f"{dirpath}/{filename}\n"
            fzf.stdin.write((line).encode())

    fzf.stdin.close()
    output, _ = fzf.communicate()
    output = output.decode()
    return output

def gcpdir(args, base_path_to_fzf):
    pass

def start_fzf(args: ArgumentParser, to_send: str)->str:
    fzf = subprocess.Popen(["fzf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = fzf.communicate(to_send.encode())
    output = output.decode()

    if args.debug:
        logging.info("Selected item: ", output)
    return output

def surf(args: ArgumentParser, basepath: str):
    """Start sidewinder, lists a directory.
    """
    # TODO add option to choose from 
    if args.basepath != "":
        cache_data(args, str_to_cache=args.basepath, fname="basepaths")
        basepath_options = load_cache_data(args, fname="basepaths")
        base_path_to_fzf = start_fzf(args, basepath_options)
        print("Base path to look inside of ",base_path_to_fzf)
        selected = localdir(args, base_path_to_fzf)
        print("Output of your selection:", selected)