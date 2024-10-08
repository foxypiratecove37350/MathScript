from cx_Freeze import setup, Executable # type: ignore
from shutil import make_archive, rmtree
import platform
import sysconfig
import mathscript
import subprocess

original_content = ""

with open('shell.py', 'r+') as f:
    content = original_content = f.read()

    try:
        git_release_tag = subprocess.check_output(['git', 'describe', '--tags']).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        git_release_tag = "latest"
    
    try:
        git_commit_hash = subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD']).decode('utf-8').strip()
    except subprocess.CalledProcessError as e:
        git_commit_hash = "latest"
    
    try:
        git_commit_date = subprocess.check_output(['git', 'show', '-s', '--format=%cd', '--date=format:"%b %e %Y, %H:%M:%S"', 'HEAD']).decode('utf-8').strip().removeprefix('"').removesuffix('"')
    except subprocess.CalledProcessError as e:
        git_commit_date = None # type: ignore

    content = content.replace("git_release_tag = 'latest'\ngit_commit_hash = 'latest'\ngit_commit_date = None", f'git_release_tag = {repr(git_release_tag)}\ngit_commit_hash = {repr(git_commit_hash)}\ngit_commit_date = {repr(git_commit_date)}')

    f.seek(0)
    f.write(content)
    f.truncate()

build_options = {'packages': [], 'excludes': []} # type: ignore

base = 'console'

executables = [
    Executable('shell.py', base=base, target_name = mathscript.product_name.lower())
]

try:
    setup(name=mathscript.product_name,
        version = mathscript.version_str,
        description = mathscript.product_description,
        options = {'build_exe': build_options},
        executables = executables)
    
    try:
        rmtree(f'build/{mathscript.product_name.lower()}_{platform.system().lower().replace('darwin', 'macos')}')
    except FileNotFoundError:
        pass
    
    make_archive(f'build/{mathscript.product_name.lower()}_{platform.system().lower().replace('darwin', 'macos')}', 'zip', f'build/exe.{sysconfig.get_platform()}-{sysconfig.get_python_version()}')
finally:
    with open('shell.py', 'w') as f:
        f.write(original_content)