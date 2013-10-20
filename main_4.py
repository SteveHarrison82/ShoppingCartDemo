import os
import sys


import webapp2


class Handler(webapp2.RequestHandler):
    def write(self, a):
        self.response.out.write(a)

    '''
    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        self.write(self.render_str(template, **kw))

    '''
class MainPage(Handler):
    def get(self):
        #self.response.headers['Content-Type'] = 'text/plain'
        myvisit=self.request.cookies.get('visits','0')
        self.write(myvisit)
        if myvisit=='0':
            myvisit=1
            self.response.headers.add_header('Set-Cookie', 'visits=%s' % myvisit)
        else:
            myvisit=int(myvisit)+1
            self.response.headers.add_header('Set-Cookie', 'visits=%s' % myvisit)
        self.write("You've been here %s times!" % myvisit)


app = webapp2.WSGIApplication([('/', MainPage)], debug=True)
