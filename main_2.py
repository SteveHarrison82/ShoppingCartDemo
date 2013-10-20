__author__ = 'ramr'
import os
import sys
sys.path.append("/usr/lib/python2.7/dist-packages")
sys.path.append("/home/ramr/Desktop/google_appengine/lib/webapp2")
import jinja2
import webapp2
from google.appengine.ext import db

'''template_dir variable is current dirname joined with folder name templates'''
template_dir = os.path.join(os.path.dirname(__file__), 'templates')



'''class jinja2.FileSystemLoader(searchpath, encoding='utf-8')
Loads templates from the file system. This loader can find templates in folders on the file system and is the preferred way to load them.

The loader takes the path to the templates as string, or if multiple locations are wanted a list of them which is then looked up in the given order:

>>> loader = FileSystemLoader('/path/to/templates')
>>> loader = FileSystemLoader(['/path/to/templates', '/other/path'])



class jinja2.Environment([options])
The core component of Jinja is the Environment. It contains important shared variables like configuration,
filters, tests, globals and others. Instances of this class may be modified if they are not
shared and if no template was loaded so far. Modifications on environments after the first template was loaded will
 lead to surprising effects and undefined behavior.

autoescape
If set to true the XML/HTML autoescaping feature is enabled by default. For more details about auto escaping
see Markup. As of Jinja 2.4 this can also be a callable that is passed the template name and has to return True or
False depending on autoescape should be enabled by default.

'''

myTemplateFolder=jinja2.FileSystemLoader(template_dir)


jinja_env = jinja2.Environment(loader = myTemplateFolder , autoescape=True)

'''
self.response.out.write(myform %{"error":error}) accepts input as string
'''

class Handler(webapp2.RequestHandler):
    def write_as_response(self,a):
        self.response.out.write(a)

    def render_str(self, myhtmltemplate, **params):
        myhtmlstring = jinja_env.get_template(myhtmltemplate)
        return myhtmlstring.render(params)

    def render_output(self,myhtmltemplate,**kw):
        #p=self.render_str(myhtmltemplate, **kw)
        self.write_as_response(str(self.render_str(myhtmltemplate, **kw)))

'''MyHomePage'''

'''
A table called Art is created in GQL
'''
class Art(db.Model):
    title=db.StringProperty(required=True)
    art=db.TextProperty(required=True)
    created=db.DateTimeProperty(auto_now_add=True)
    

class MyHomePage(Handler):
    def render_front(self,title="",art="",error=""):
        arts=db.GqlQuery("select * from Art order by created desc")
        self.render_output("front.html",title=title,art=art,error=error,arts=arts)
        #self.render_output("front.html", title=title,  art)
    def get(self):
        self.render_front()
    def post(self):
        title=self.request.get("title")
        art=self.request.get("art")
        if title and art:
            a=Art(title=title, art=art)
            a.put()

            self.redirect('/')
        else:
            error="we need both a title and some artwork!"
            self.render_front(title,art,error)



app = webapp2.WSGIApplication([('/', MyHomePage)], debug=True)

