import sys, os
virtualenv_path = "/home/nonzer0/.virtualenvs/wagtail"
PROJECT_SETTINGS = "cms.settings.production"
PROJECT_DIR = "src"

INTERP = virtualenv_path + "/bin/python"
#INTERP is presented twice so that the new Python interpreter knows the actual executable path.
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

cwd = os.getcwd()
sys.path.append(os.path.join(cwd, PROJECT_DIR))

os.environ['DJANGO_SETTINGS_MODULE'] = PROJECT_SETTINGS
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
