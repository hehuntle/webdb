from wsgiref.simple_server import make_server
from pyramid.config import Configurator
#from pyramid.response import FileResponse # note it's FileResponse instead of Response
from pyramid.renderers import render_to_response

import mysql.connector as mysql
import os

db_user = os.environ['MYSQL_USER']
db_pass = os.environ['MYSQL_PASSWORD']
db_name = os.environ['MYSQL_DATABASE']
#db_host = os.environ['MYSQL_HOST']
db_host = 'localhost'

def home(req):
    return render_to_response('templates/lp.html', {}, request=req)

def sufirst(req):
    if req.method=="GET":
        return render_to_response('templates/su1.html', {}, request=req)
    elif req.method=="POST":

        first_name=req.POST[first_name]
        last_name=req.POST[last_name]
        email=req.POST[email]
        db = mysql.connect(user=db_user, password=db_pass, host=db_host, database=db_name)
        cursor = db.cursor()

        query = "insert into Users (first_name, last_name, email) values (%s, %s, %s)"
        values = (first_name, last_name, email)

        cursor.execute(query, values)
        db.commit()
        return render_to_response('templates/su2.html', {}, request=req)


def susecond(req):
    return render_to_response('templates/su2.html', {}, request=req)

def fea(req):
    return render_to_response('templates/f.html', {}, request=req)

def price(req):
    return render_to_response('templates/pricing.html', {}, request=req)

def about(req):
    return render_to_response('templates/au.html', {}, request=req)


if __name__ == '__main__':
    with Configurator() as config:

        config.include('pyramid_jinja2')
        config.add_jinja2_renderer('.html')

        config.add_route('home', '/lp')
        config.add_view(home, route_name='home')

        config.add_route('sn', '/sign')
        config.add_view(sufirst, route_name='sn')
        config.add_view(susecond, route_name='sn', request_method='POST')

        config.add_route('ab', '/about')
        config.add_view(about, route_name='ab')

        config.add_route('pricing', '/pricing')
        config.add_view(price, route_name='pricing')

        config.add_route('feature', '/feature')
        config.add_view(fea, route_name='feature')

        config.add_static_view(name='/', path='./public', cache_max_age=3600) #expose the public folder for the CSS file
        app = config.make_wsgi_app()

    server = make_server('0.0.0.0', 5000, app)
    server.serve_forever()
