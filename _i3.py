from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Integer, Key, Text, RunCommand, Choice, Function
from language import *

grammar = Grammar("i3")

def i3_change_workspace(n):
    RunCommand(f"i3-msg \"workspace {n}\"").execute()

def i3_launch_app(app):
    RunCommand(f"i3-msg \"exec {app}\"").execute()


def i3_fullscreen():
    RunCommand(f"i3-msg \"fullscreen\"").execute()

rule_map_language = {
    "en": {
        "i three workspace <n>": Function(i3_change_workspace),
        "i three launch <app>": Function(i3_launch_app),
        "i three full screen": Function(i3_fullscreen),
    },
    "fr": {
        "i trois bureau <n>": Function(i3_change_workspace),
        "i trois lance <app>": Function(i3_launch_app),
        "i trois plein écran": Function(i3_fullscreen),
    },
}

i3_rule = MappingRule(
    name = "i",
    mapping = rule_map_language[LANGUAGE],
    extras = [
        IntegerRef("n", 1, 10),
        Choice("app", {
            "firefox": "firefox",
            "discord": "discord",
            "thunderbird": "thunderbird",
            "(terminal | term)": "urxvt",
            "stats": "urxvt -e $SHELL -c 'htop'",
            "directory": "pcmanfm",
            "pacman": "pamac-manager",
        })
    ])

grammar.add_rule(i3_rule)
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

