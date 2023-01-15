from commander.args.arg_parse_rules import *

# should_default_be_added(settings: dict, arg_parse_params: dict)->dict:

# arg_settings = {'required': False, 'flags': {'small_form': '-b', 'long_form': '--basepath'}, 'action': '', 'help': 'A flag to predefine basepath', 'type': 'int', 'default': '', 'nargs': '+', 'choices': []}
# kwargs = {"help": arg_settings["help"], "required": arg_settings["required"]}

def test_should_default_be_added():
    kwargs = {}
    arg_settings = {'action': '', 'default': 'test'}
    assert should_default_be_added(arg_settings, kwargs) == {'default': 'test'}
    arg_settings = {'action': '', 'default': 'default behavior here'}
    assert should_default_be_added(arg_settings, kwargs) == {'default': 'default behavior here'}

def test_should_action_be_added():
    kwargs = {}
    arg_settings = {'action': 'store_true'}
    assert should_action_be_added(arg_settings, kwargs) == {'action': 'store_true'}
    arg_settings['action'] = 'test'
    assert should_action_be_added(arg_settings, kwargs) == {'action': 'test'}

def test_should_type_be_added():
    kwargs = {}
    arg_settings = {'action': 'test', 'type': 'int'}
    assert should_type_be_added(arg_settings, kwargs) == {'type': int}
    arg_settings['type'] = 'str'
    assert should_type_be_added(arg_settings, kwargs) == {'type': str}

def test_should_choice_be_added():
    kwargs = {}
    arg_settings = {'action': 'x', 'choices': ['choice1', 'choice2']}
    assert should_choice_be_added(arg_settings, kwargs) == {'choices': ['choice1', 'choice2']}
    arg_settings = {'action': 'x', 'choices': ['sample2']}
    assert should_choice_be_added(arg_settings, kwargs) == {'choices': ['sample2']}

    arg_settings = {'action': '', 'choices': ['sample2']}
    assert should_choice_be_added(arg_settings, kwargs) == {}
    arg_settings = {'action': 'x', 'choices': []}
    assert should_choice_be_added(arg_settings, kwargs) == {}



def should_choice_be_added(settings: dict, arg_parse_params: dict)->dict:
    if settings['choices'] != [] and settings['action'] == '':
        arg_parse_params.update({"choices": settings['choices']})
    return arg_parse_params