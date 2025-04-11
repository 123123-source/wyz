import os, shutil
from datetime import datetime
from app import create_app, freezer, pages
import click
from flask.cli import with_appcontext

app = create_app(os.getenv('FLASK_CONFIG') or 'default')

@app.cli.command("freeze")
@click.option('--debug', is_flag=True)
def freeze_command(debug):
    """Generate static site."""
    if debug:
        freezer.run(debug=True)
    freezer.freeze()

from config import basedir
pagesdir = os.path.join(basedir, 'app/pages')

@app.cli.command("new-post")
@click.argument('title')
def new_post_command(title):
    """Create a new blog post."""
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    yaml_header = f'title: {title}\ndate: {current_time}\n\n'
    
    filename = title.replace(' ','_') + '.md'
    filepath = os.path.join(pagesdir, filename)
    with open(filepath, 'w', encoding='utf-8') as thefile:
        thefile.write(yaml_header)
    os.system(f"subl {filepath}")

@app.cli.command("publish")
@click.option('--push', is_flag=True)
@click.option('--remote', default='origin')
@click.option('--branch', default='master')
def publish_command(push, remote, branch):
    """Publish blog posts."""
    freezer.freeze()

    for page in pages:
        os.system(f'git add {page.path}')
    os.system(f'git add {os.path.join(basedir,"app/pages/")}')
    for page in pages:
        os.system(f'git add {os.path.join(basedir, page.path)}')
    
    commit_msg = f'publishing articles {" ".join([page.path for page in pages])}'
    os.system(f'git commit -m "{commit_msg}"')
    
    if push or click.confirm(f"Push from branch '{branch}' to remote '{remote}'?"):
        os.system(f'git push {remote} {branch}')

@app.cli.command("remove")
@click.argument('filename')
@click.option('--push', is_flag=True)
@click.option('--remote', default='origin')
@click.option('--branch', default='master')
def remove_command(filename, push, remote, branch):
    """Remove a blog post."""
    try: 
        filepath = os.path.join(basedir, f'app/pages/{filename}.md')
        os.remove(filepath)
        os.system(f'git add -u {filepath}')
    except OSError:
        print(f'"{filename}.md" does not exist or has been removed')
    
    try: 
        dirpath = os.path.join(basedir, filename)
        shutil.rmtree(dirpath)
        os.system(f'git add -u {dirpath}')
    except OSError:
        print(f'"{filename}" does not exist or has been removed')
    
    os.system(f'git commit -m "removed {filename}"')
    
    if push or click.confirm(f"Push from branch '{branch}' to remote '{remote}'?"):
        os.system(f'git push {remote} {branch}')

if __name__ == '__main__':
    app.cli()