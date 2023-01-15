import os
import editor
import subprocess
from logger import *
from constants import OPTIONS
from prompt_toolkit import prompt
from prompt_toolkit.key_binding.vi_state import InputMode
from prompt_toolkit.completion import Completer, Completion, ThreadedCompleter
from argparse import ArgumentParser
from walker.datacache import cache_data, load_cache_data

class SideCompletion(Completer):
    def __init__(self):
        self.options = []

    def get_completions(self, document, complete_event):
        # Provide custom autocomplete suggestions based on the current input
        word_before_cursor = document.get_word_before_cursor(WORD=True)
        if word_before_cursor:
            # word starts with 'f'
            try:
                if(word_before_cursor.startswith('gs://')):
                    # TODO self.options = gcp.listdir
                    pass
                else:
                    self.options = os.listdir(word_before_cursor)
            except:
                pass

            last_word = word_before_cursor.split('/')[-1:][0]


            for opt in self.options:
                if last_word in opt:
                    rest_of_word = opt[len(last_word):]
                    yield Completion(rest_of_word)

def localdir(args: ArgumentParser, base_path_to_fzf: str)->str:
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

def mv_logic(args: ArgumentParser, action:str, base_path_to_fzf: str)->tuple[str, str]:
        left_selected: str = localdir(args, base_path_to_fzf) 
        right_selected: str = localdir(args, base_path_to_fzf).strip()

        side_winder_completer = SideCompletion()
        thread_completer = ThreadedCompleter(side_winder_completer)
        if args.vim == True:
            right_selected = prompt("Move to: ", default=right_selected.replace('\n', ''), completer=thread_completer, vi_mode=True)
        else: 
            right_selected = prompt("Move to: ", default=right_selected.replace('\n', ''), completer=thread_completer,)
        return left_selected, right_selected

def cp_logic(args: ArgumentParser, action:str, base_path_to_fzf: str)->tuple[str, str]:
        left_selected: str = localdir(args, base_path_to_fzf) # TODO add OPEN in browser option
        right_selected: str = localdir(args, base_path_to_fzf).strip()
        if args.vim == True:
            right_selected = prompt("Copy to: ", default=right_selected.replace('\n', ''), vi_mode=True)
        else: 
            right_selected = prompt("Copy to: ", default=right_selected.replace('\n', ''))
        return left_selected, right_selected

def rm_logic(args: ArgumentParser, action:str, base_path_to_fzf: str)->tuple[str, str]:
        left_selected: str = localdir(args, base_path_to_fzf) # TODO add OPEN in browser option
        right_selected: str = ""
        return left_selected, right_selected

def action_logic(args: ArgumentParser, action: str, base_path_to_fzf: str)->str:
    left_selected = ""
    right_selected = ""
    if action.startswith("mv"):
        left_selected, right_selected = mv_logic(args, action, base_path_to_fzf)
    elif action.startswith("cp"):
        left_selected, right_selected = cp_logic(args, action, base_path_to_fzf)
    elif action.startswith("rm"):
        left_selected, right_selected = rm_logic(args, action, base_path_to_fzf)
    else:
        print(f"Invalid movement option: {action}")

    cmd = f"gsutil -m {action} {left_selected} {right_selected}".replace('\n', ' ')
    return cmd


def surf(args: ArgumentParser, basepath: str):
    """Start sidewinder, lists a directory.
    """
    if args.basepath != "":
        cache_data(args, str_to_cache=args.basepath, fname="basepaths")
        basepath_options = load_cache_data(args, fname="basepaths")
        base_path_to_fzf = start_fzf(args, basepath_options)
        print("Base path to look inside of ",base_path_to_fzf)

        action: str = start_fzf(args, OPTIONS)
        result_cmd = action_logic(args, action, base_path_to_fzf)

        if args.vim == True:
            result_cmd = prompt("Run this command? ", default=result_cmd, vi_mode=True)
        else: 
            result_cmd = prompt("Run this command? ", default=result_cmd)

        # TODO os.exec(result_cmd)
        print("Executed", result_cmd)