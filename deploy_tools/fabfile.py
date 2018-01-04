from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run
import random

REPO_URL = 'https://github.com/avc/cms.git'

def deploy():
    site_folder = f'/home/{env.user}/{env.host}'
    source_folder_name = 'src'
    source_folder = f'{site_folder}/{source_folder_name}'
    project_name = 'cms'
    virtualenv = "/home/nonzer0/.virtualenvs/wagtail"
    
    #_create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_virtualenv(source_folder, virtualenv)
    _update_secret_key(source_folder, env.host, project_name)
    _update_static_files(source_folder, virtualenv)
    _update_database(source_folder, virtualenv)
    _link_wsgi(site_folder, source_folder_name)
    
def _create_directory_structure_if_necessary(site_folder):
    for subfolder in ('db', 'public/static', 'src'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
    else:
        run(f'git clone {REPO_URL} {source_folder}')
    current_commit = local('git log -n 1 --format=%H', capture=True)
    run(f'cd {source_folder} && git reset --hard {current_commit}')
    
def _update_settings(source_folder, host, project_name):
    # Debug false
    settings_file = f'{source_folder}/{project_name}/settings/production.py'
    sed(settings_file, 'DEBUG = True', 'DEBUG = False')
    sed(settings_file, 
        'ALLOWED_HOSTS = .+$', 
        f'ALLOWED_HOSTS = ["{host}"]'
    )

def _update_secret_key(source_folder, host, project_name):
    # Secret key
    secret_key_file = f'{source_folder}/{project_name}/settings/secret_key.py'
    if not exists(secret_key_file):
        chars = "abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)"
        secret_key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{secret_key}"')
    
def _update_virtualenv(source_folder, virtualenv):
    if not exists(f'{virtualenv}/bin/pip'):
        run(f'python3 -m venv {virtualenv}')
    run(f'{virtualenv}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder, virtualenv):
    run(
        f'cd {source_folder}'
        f' && {virtualenv}/bin/python manage.py collectstatic --noinput'
    )
    
def _update_database(source_folder, virtualenv):
    run(
        f'cd {source_folder}'
        f' && {virtualenv}/bin/python manage.py migrate --noinput'
    )
    
def _link_wsgi(site_folder, source_folder_name):
    relative_wsgi_file_path = f'{source_folder_name}/deploy_tools/wsgi.py'
    run(
        f'cd {site_folder}'
        f' && ln -sf {relative_wsgi_file_path} passenger_wsgi.py'
    )
    run(f'mkdir -p {site_folder}/tmp')
    run(f'touch {site_folder}/tmp/restart.txt')
