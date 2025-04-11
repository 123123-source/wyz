from flask import render_template
from . import main
from .. import pages, freezer


@main.route('/')
def home():
    posts = [page for page in pages]
    # Sort pages by date
    sorted_posts = sorted(posts, reverse=True,
        key=lambda page: page.meta['date'])
    return render_template('home.html', pages=sorted_posts)

@main.route('/<path:path>/')
def page(path):
    # 'path is the filename of a page, without the file extension'
    # e.g. "first-post"
    page = pages.get_or_404(path)
    return render_template('page.html', page=page)

@main.route('/project')
def project():
    return render_template('project.html')

@main.route('/teaching')
def teaching():
    return render_template('teaching.html')

@main.route('/team')
def team():
    return render_template('team.html')

@main.route('/registration')
def registration():
    return render_template('registration.html')
