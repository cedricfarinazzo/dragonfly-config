"""
Command-module loader for CMU Pocket Sphinx.

This script is based on 'dfly-loader-wsr.py' written by Christo Butcher and
has been adapted to work with the Sphinx engine instead.

This script can be used to look for Dragonfly command-modules for use with
the CMU Pocket Sphinx engine. It scans the directory it's in and loads any
``_*.py`` it finds.
"""


# TODO Have a simple GUI for pausing, resuming, cancelling and stopping
# recognition, etc

from language import *
import logging
import os.path
import sys

import six

from dragonfly import get_engine, RecognitionObserver
from dragonfly.loader import CommandModuleDirectory
from dragonfly.log import setup_log

# --------------------------------------------------------------------------
# Set up basic logging.

setup_log()


# --------------------------------------------------------------------------
# Main event driving loop.

def main():
    try:
        path = os.path.dirname(__file__)
    except NameError:
        # The "__file__" name is not always available, for example
        # when this module is run from PythonWin.  In this case we
        # simply use the current working directory.
        path = os.getcwd()
        __file__ = os.path.join(path, "sphinx_module_loader.py")

    # Initialize the engine.
    engine = get_engine("sphinx")

    # Try to import the local engine configuration object first. If there isn't one,
    # use the default engine configuration.
    log = logging.getLogger("config")
    try:
        import config
        engine.config = config
        log.info("Using local engine configuration module 'config.py'")
    except ImportError:
        pass
    except Exception as e:
        # Log errors caught when setting the configuration.
        log.exception("Failed to set config using 'config.py': %s" % e)
        log.warning("Falling back to the default engine configuration")

    # You can also set any configuration options here instead of using a
    # config.py file. For example:
    engine.config.START_ASLEEP = False
    engine.config.DECODER_CONFIG.set_float("-vad_threshold", 3.1)
    engine.config.LANGUAGE = LANGUAGE

    # Call connect() now that the engine configuration is set.
    engine.connect()

    # Load grammars.
    directory = CommandModuleDirectory(path, excludes=[__file__])
    directory.load()

    class Observer(RecognitionObserver):
        def on_begin(self):
            print("=> Speech start detected.")

        def on_recognition(self, words):
            message = u"Recognized: %s" % u" ".join(words)
            print("=>", message)

        def on_failure(self):
            print("=> Sorry, what was that?")

    observer = Observer()
    observer.register()

    # Start the engine's main recognition loop
    try:
        engine.recognise_forever()
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
