import os 
import sys
import msvcrt
import select
import subprocess
from typing import List

def collect_pipe_input()->str:
    """Collect platform specific standard input text, i.e. from | 

    Returns:
        str: Mutliline str of data from pipe.
    """
    std_in_text = ""
    for line in sys.stdin:
        std_in_text += line
    return std_in_text

def start_fzf(to_send: str)->str:
    fzf = subprocess.Popen(["fzf"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    output, _ = fzf.communicate(to_send.encode())
    output = output.decode()
    print("Selected item: ", output)
    return output

def entry_point(std_in_text: str, args: List[str]):
    """Commandline args to pass to the program.
    Examples: --vi enables vim keybinds.
    Or standard input from | char

    Args:
        args (List[str]): program arguments to enable certain settings.
    """
    if std_in_text != "":
        start_fzf(std_in_text)
    else:
        print("nothing to do")





if __name__ == "__main__":
    entry_point(collect_pipe_input(), [])
