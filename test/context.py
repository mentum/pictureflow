import os
import sys
# This procedure is necessary so that it's possible to import the pictureflow module from the tests without keeping the
# tests in the pictureflow module
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pictureflow as pf
