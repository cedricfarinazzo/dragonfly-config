from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Integer, Key, Text, RunCommand

grammar = Grammar("i3")

class WorkspaceRule(MappingRule):
    name = "i3"
    mapping = {
        "workspace <n>": None
    }
    extras = [
        IntegerRef("n", 1, 9)
    ]

    def _process_recognition(self, value, extras):
        n = extras["n"]
        RunCommand(f"i3-msg \"workspace {n}\"").execute()


grammar.add_rule(WorkspaceRule())
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

