import os

from google.appengine.ext import webapp
#import webapp2



months = ["January",
          'February',
          'March',
          'April',
          'May',
          'June',
          'July',
          'August',
          'September',
          'October',
          'November',
          'December']

def valid_month(month):
    if month.capitalize() in months:
        k=month.capitalize()
    else:
        print months
        k=None
    return k

def valid_day(day):
    if day and day.isdigit():
        myday=int(day)
        print 'hallo'
        if (myday>0) and (myday <= 31):
            k=myday
            return k
        else:
            return None


def valid_year(year):
    if year and year.isdigit():
        myyear=int(year)
        #print 'hallo'
        if (myyear>1900) and (myyear <= 1998):
            k=myyear
            return k
        else:
            return None

myform="""<form method="post" action="/">
<label>What is your birthday ?</label>
<br>
<label>Month
<input type="text" name="month">
</label>
<label> Day
<input type="text" name="day">
</label>
<label>Year
<input type="text" name="year">
</label>
<br>
<input type="submit">
<br>
<div>%(error)s</div>
</form>"""


class MyHomePage(webapp.RequestHandler):
    def get(self):
        #self.response.headers['Content-Type']='text/html'
        self.response.out.write(myform)
    def post(self):
        the_month=self.request.get("month")
        the_year=self.request.get("year")
        the_day=self.request.get("day")
        validfy_month=valid_month(the_month)
        validfy_year=valid_year(the_year)
        validfy_day=valid_day(the_day)

        if (validfy_month and validfy_year and validfy_day):
            self.redirect("/thanks")
        else:
            error="Thats not a invalid input my friend"
            self.write_form(myform,error)

    def write_form(self,myform,error):
        self.response.out.write(myform %{"error":error})

class MyThankyouPage(MyMainPage):
    def get(self):
        self.response.out.write("thats a valid input, thank you")

'''class MyTestPage(webapp.RequestHandler):
    def post(self):
        self.response.headers['Content-Type']='text/plain'
        #myq=self.request.get("q")
        self.response.out.write(self.request)
'''
app = webapp.WSGIApplication([('/', MyHomePage),('/thanks',MyThankyouPage)],
    debug=True)
