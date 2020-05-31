from dragonfly import Grammar, AppContext, MappingRule, Dictation, \
        IntegerRef, Key, Text, get_engine, Function

grammar = Grammar("dragon")

def disconnect():
    print("Disconnecting engine.")
    engine = get_engine()
    if engine.name == 'natlink' and 'natspeak' in sys.executable:
        print("Not calling disconnect() for embedded natlink.")
    else:
        engine.disconnect()

dragon_rule = MappingRule(
    name = "dragon",
    mapping = {
        "dragon off": Function(disconnect),
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

