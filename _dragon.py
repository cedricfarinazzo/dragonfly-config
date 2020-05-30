from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Key, Text

grammar = Grammar("dragon")

dragon_rule = MappingRule(
    name = "dragon",
    mapping = {
        "dragon off": Key("npdiv"),
    },
    extras = []
)

grammar.add_rule(dragon_rule)
grammar.load()

def unload():
    global grammar
    if grammar:
        grammar.unload()
    grammar = None

