import sys
import os


project_home = '/home/egarestu/velyn_bot'
if project_home not in sys.path:
    sys.path.insert(0, project_home)


from main import app as application