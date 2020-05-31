from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Integer, Key, Text, RunCommand, Choice, Function

grammar = Grammar("i3")

def i3_change_workspace(n):
    RunCommand(f"i3-msg \"workspace {n}\"").execute()

def i3_launch_app(app):
    RunCommand(f"i3-msg \"exec {app}\"").execute()


class I3Rule(MappingRule):
    mapping = {
        "i workspace <n>": Function(i3_change_workspace),
        "i launch <app>": Function(i3_launch_app)
    }
    extras = [
        IntegerRef("n", 1, 10),
        Choice("app", {
            "firefox": "firefox",
            "discord": "discord",
            "thunderbird": "thunderbird",
            "(terminal | term)": "urxvt",
            "stats": "urxvt -e $SHELL -c 'htop'",
            "dir": "pcmanfm",
            "pacman": "pamac-manager",
        })
    ]

grammar.add_rule(I3Rule())
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

