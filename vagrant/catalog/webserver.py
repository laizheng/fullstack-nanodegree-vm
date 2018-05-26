from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer
import cgi
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, MenuItem, Restaurant
import re

htmlMain = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <a href="/resturant/new">Make a New Resturant Here</a><br><br>
    %s
  </body>
</html>
"""

htmlCreateNewRestaurant = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <form method='POST' enctype="multipart/form-data" action = "/resturant/new">
        <h1>Make A New Restaurant</h1>
        <input enctype='multipart/form-data' name="RestaurantName" type="text" placeholder="New Restaurant Name">
        <input type="submit" value="Create">
    </form>
  </body>
</html>
"""

htmlEditRestaurant = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <form method='POST' enctype="multipart/form-data" action="{}">
        <h2>{}</h2>
        <input enctype='multipart/form-data' name="RestaurantName" type="text" placeholder="{}">
        <input type="submit" value="Rename">
    </form>
  </body>
</html>
"""

htmlDeleteRestaurant = r"""<!DOCTYPE html>
<html lang="en" dir="ltr">
  <head>
    <meta charset="utf-8">
    <title></title>
  </head>
  <body>
    <form method='POST' enctype="multipart/form-data" action="{}">
        <h2>Are you sure you want to delete {}?</h2>
        <input type="submit" value="Delete">
    </form>
  </body>
</html>
"""

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class webServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/resturant"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = ""
                for row in session.query(Restaurant).all():
                    output += row.name + "<br/>" + \
                              '<a href="%s/edit">edit</a><br>' % (self.path + "/" + str(row.id)) \
                              + '<a href="%s/delete">delete</a><br><br>' % (self.path + "/" + str(row.id))
                output = htmlMain % output
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/resturant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = htmlCreateNewRestaurant
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/edit"):
                p = re.compile(r"/(\d+)/edit")
                m = p.search(self.path)
                if m == None:
                    raise IOError
                id = int(m.group(1))
                theRestaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = htmlEditRestaurant.format(self.path, theRestaurant.name, theRestaurant.name)
                self.wfile.write(output)
                print output
                return
            if self.path.endswith("/delete"):
                id = int(self.path.split("/")[2])
                theRestaurant = session.query(Restaurant).filter_by(id=id).one()
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                output = htmlDeleteRestaurant.format(self.path, theRestaurant.name)
                self.wfile.write(output)
                print output
                return
        except IOError:
            self.send_error(404, 'File Not Found: %s' % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/resturant/new"):
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('RestaurantName')[0]
                    new_restaurant = Restaurant(name=new_restaurant_name)
                    session.add(new_restaurant)
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", "/resturant")
                self.end_headers()
            if self.path.endswith("/edit"):
                p = re.compile(r"/(\d+)/edit")
                m = p.search(self.path)
                if m == None:
                    raise IOError
                id = int(m.group(1))
                ctype, pdict = cgi.parse_header(
                    self.headers.getheader('content-type'))
                if ctype == 'multipart/form-data':
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('RestaurantName')[0]
                    restaurant = session.query(Restaurant).filter_by(id=id).one()
                    restaurant.name = new_restaurant_name
                    session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", "/resturant")
                self.end_headers()
            if self.path.endswith("/delete"):
                id = int(self.path.split("/")[2])
                theRestaurant = session.query(Restaurant).filter_by(id=id).one()
                session.delete(theRestaurant)
                session.commit()
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header("Location", "/resturant")
                self.end_headers()
        except IOError:
            self.send_error(404, 'Error when parsing update request! path: %s' % self.path)
        except:
            pass


def main():
    try:
        port = 8080
        server = HTTPServer(('', port), webServerHandler)
        print "Web Server running on port %s" % port
        server.serve_forever()
    except KeyboardInterrupt:
        print " ^C entered, stopping web server...."
        server.socket.close()

if __name__ == '__main__':
    main()
