import os
import sys

# Keep the modules directory on sys.path so bare imports (from tests and
# direct script invocation) continue to work while we transition to relative
# imports.  This shim will be removed once all imports are fully relative.
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

__app_name__ = "Vocabulary Builder CLI"
__version__ = "2.0.0"
