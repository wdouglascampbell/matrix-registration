# Defined before the submodule imports below so __version__ is always available
# even if a submodule references it during package initialization.
__version__ = "1.0.2"
name = "matrix_registration"

from . import api
from . import tokens
from . import config
