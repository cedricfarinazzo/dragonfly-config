from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Integer, Key, Text, RunCommand, Choice

grammar = Grammar("i3")

class WorkspaceRule(MappingRule):
    name = "workspace"
    mapping = {
        "i workspace <n>": None
    }
    extras = [
        IntegerRef("n", 1, 9)
    ]

    def _process_recognition(self, value, extras):
        n = extras["n"]
        RunCommand(f"i3-msg \"workspace {n}\"").execute()

class LaunchRule(MappingRule):
    name = "launch"
    mapping = {
        "i launch <text>": None
    }
    extras = [
        Choice("text", {
            "firefox": "firefox",
            "discord": "discord",
            "thunderbird": "thunderbird",
            "(terminal | term)": "urxvt",
            "stats": "urxvt -e $SHELL -c 'htop'",
            "dir": "pcmanfm",
            "pacman": "pamac-manager",
        })
    ]

    def _process_recognition(self, value, extras):
        cmd = extras["text"]
        RunCommand(f"i3-msg \"exec {cmd}\"").execute()


grammar.add_rule(WorkspaceRule())
grammar.add_rule(LaunchRule())
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

