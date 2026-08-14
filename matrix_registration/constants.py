# Standard library imports...
import os
import sys


def _user_config_dir(app):
    """Per-user config dir, XDG spec, stdlib-only.

    Replaces the former appdirs.user_config_dir dependency (appdirs is
    unmaintained/deprecated) with the one XDG rule this app needs: honor
    $XDG_CONFIG_HOME, else ~/.config.
    """
    base = os.environ.get("XDG_CONFIG_HOME") or os.path.expanduser("~/.config")
    return os.path.join(base, app)


__location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
WORD_LIST_PATH = os.path.join(__location__, "wordlist.txt")
CONFIG_SCHEMA_PATH = os.path.join(__location__, "config.schema.json")
# first check in current working dir
CONFIG_PATH1 = os.path.join(os.getcwd() + "/")
CONFIG_PATH2 = os.path.join(os.getcwd() + "/config/")
# then check in XDG_CONFIG_HOME
CONFIG_PATH3 = os.path.join(_user_config_dir("matrix-registration") + "/")
# check at installed location
CONFIG_PATH4 = os.path.join(__location__, "../")
CONFIG_PATH5 = os.path.join(sys.prefix, "config/")
