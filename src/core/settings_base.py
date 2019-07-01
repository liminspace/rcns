import sys
from unipath import Path


BASE_DIR = Path(__file__).absolute().ancestor(2)  # django project dir (src)
ROOT_DIR = BASE_DIR.parent                        # repository root dir
LOG_DIR = ROOT_DIR.child('var', 'log')            # log dir
TMP_DIR = ROOT_DIR.child('var', 'tmp')            # tmp dir

sys.path.append(ROOT_DIR.child('conf'))
try:
    import local_settings
    ls = local_settings.__dict__
except ImportError:
    raise RuntimeError('Please, provide your local configuration for this project.\n'
                       'You need to create conf/local_settings.py with your local settings.')
finally:
    sys.path.pop()
