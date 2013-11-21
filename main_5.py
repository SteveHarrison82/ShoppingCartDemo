__author__ = 'ramr'
import random
import os
import sys
sys.path.append("/usr/lib/python2.7/dist-packages")
sys.path.append("/home/ramr/Desktop/google_appengine/lib/webapp2")
import jinja2
import webapp2
from google.appengine.ext import db

'''template_dir variable is current dirname joined with folder name templates'''
template_dir = os.path.join(os.path.dirname(__file__),'templates')
'''
The loader takes the path to the templates as string, or if multiple locations are wanted
a list of them which is then looked up in the given order:

>>> loader = FileSystemLoader('/path/to/templates')
>>> loader = FileSystemLoader(['/path/to/templates', '/other/path'])


'''
myTemplateFolder=jinja2.FileSystemLoader(template_dir)
jinja_env = jinja2.Environment(loader = myTemplateFolder , autoescape=True)

'''
self.response.out.write(myform %{"error":error}) accepts input as string
'''

'''render_str = render string from my template folder'''




class StoreCredentials(db.Model):
    UserID=db.StringProperty(required=True)
    Password=db.StringProperty(required=True)


class CartedProduct(db.Model):
    User_with_Cart=db.ReferenceProperty(StoreCredentials)
    Carted_Sku=db.StringProperty(required=True)
    Quantity_carted=db.IntegerProperty(required=True)


class AvailableProductsCatalog(db.Model):
    Product_Name=db.StringProperty(required=True)
    Sku_Number=db.StringProperty(required=True)
    Price=db.StringProperty(required=True)
    Product_image_url=db.StringProperty(required=False)
    Product_Attribute=db.StringProperty(required=True)


def init_db_with_items():
    if len(AvailableProductsCatalog)==0
        Addproduct1=AvailableProductsCatalog(Product_Name='RamaDE',
        Sku_Number='rama_1',
        Price='25e-dollar',
        Product_image_url='/images/butter/rama-de.jpeg',
        Product_Attribute='25g butter')
        Addproduct1.put()

        Addproduct2=AvailableProductsCatalog(Product_Name='RamaAT',
        Sku_Number='rama_2',
        Price='20e-dollar',
        Product_image_url='/images/butter/rama-at.jpeg',
        Product_Attribute='30g butter')
        Addproduct2.put()

        Addproduct3=AvailableProductsCatalog(Product_Name='Rama-Classic',
        Sku_Number='rama_3',
        Price='40e-dollar',
        Product_image_url='/images/butter/rama-classic.jpeg',
        Product_Attribute='40g butter')
        Addproduct3.put()
    return None



class Handler(webapp2.RequestHandler):

    def write_as_response(self,a):
       self.response.out.write(a)

    def render_str(self, myhtmltemplate,**params):
        myhtmlstring = jinja_env.get_template(myhtmltemplate)
        print myhtmlstring.render(params)
        return myhtmlstring.render(params)


    def render_output(self,myhtmltemplate,**kw):

        #print self.render_str(myhtmltemplate, **kw)
        self.write_as_response(str(self.render_str(myhtmltemplate, **kw)))

class LoginPage(Handler):
    def render_front(self,error1="", error2="",errorlogin="",userid=""):
        self.render_output("LoginPage.html",error1=error1, error2=error2, errorlogin=errorlogin, userid=userid)

    def get(self):
        mysession=str(random.randrange(999999))
        self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) + '; Path=/')
        self.render_front()

    def post(self):
        customerRegisterid=self.request.get('registerbutton')
        customerLoginid=self.request.get('loginbutton')
        mysession=self.request.cookies.get('session','0')


        if customerRegisterid=='Submit':
            error2=''
            customerUserid=self.request.get('userid')
            customerPwd=self.request.get('pwd')
            customerRepeatPwd=self.request.get('repeatpwd')
            if customerUserid and customerPwd and customerRepeatPwd !=None:
                if customerPwd == customerRepeatPwd:
                    CheckNewUserExist=StoreCredentials.gql("WHERE UserID = :1", customerUserid).fetch(1)
                    if CheckNewUserExist.count()==0:
                        a=StoreCredentials(UserID=customerUserid, Password=customerPwd)
                        a.put()
                        mysession=str(mysession)+'-'+customerUserid
                        self.response.headers.add_header('Set-Cookie', 'session='+mysession+ '; Path=/')
                        self.redirect('/ourproducts')

                    else:
                        error1="UserID Already Exist"
                        self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) + '; Path=/')
                        self.render_front( error1=error1, error2='',errorlogin='', userid='')
                else:
                    error2="Passwords donot match"
                    mysession=mysession+'-'+customerUserid
                    self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) + '; Path=/')
                    self.render_front( error1='', error2=error2,errorlogin='', userid=customerUserid)
            else:
                error1="UserID or Password is missing"
                self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) + '; Path=/')
                self.render_front(error1=error1, error2='',errorlogin='', userid='')

        if customerLoginid=='Submit':
            theuser=self.request.get('userid-login')
            thepass=self.request.get('pwd-login')
            verifylogincredential=db.GqlQuery('select *  from  StoreCredentials')

            for result in verifylogincredential:
                print result.UserID,result.Password

            verifylogincredential2=StoreCredentials.gql("WHERE UserID = :1 and Password=:2", theuser, thepass)
            for result2 in verifylogincredential2:
                if result2.Password==thepass:
                    mysession=str(mysession)+'-'+theuser
                    self.response.headers.add_header('Set-Cookie', 'session='+str(mysession)+ '; Path=/')
                    self.redirect('/ourproducts')

            errorlogin="UserID or Password is wrong"
            self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) +'; Path=/')
            self.render_front( error1='', error2='',errorlogin=errorlogin, userid='')


class MyProductPage(Handler):
    def render_product(self,productdisplaypage=''):
        self.render_output("ProductDisplayPage.html",productdisplaypage=productdisplaypage)

    def get(self):
        mysession=self.request.cookies.get('session','0')
        productdisplaypage=db.GqlQuery('select * from  AvailableProductsCatalog  limit 10')
        #print producttodisplay
        self.response.headers.add_header('Set-Cookie', 'session='+str(mysession)+'; Path=/')
        self.render_product(productdisplaypage)
    def post(self):
        pass


class MyCartPage(Handler):

    def getCurrentUser(self,UserIDfromCookie):
        #print UserIDfromCookie
        CurrentUserExist=StoreCredentials.gql("WHERE UserID = :1", UserIDfromCookie).get()
        return CurrentUserExist


    def post(self):
        GetSkuNumber=self.request.get('BuyNow')
        mysession=self.request.cookies.get('session','0')
        UserIDfromCookie=str(mysession).split('-',1)[1]
        p=self.getCurrentUser(UserIDfromCookie)
        print p
        if p !=None:
            k=CartedProduct(User_with_Cart=p,Carted_Sku=GetSkuNumber,Quantity_carted=1)
            k.put()
            self.redirect('/itemscarted')
        else:
            self.response.out.write("There is some problem with your cart")


class Checkout(Handler):
    pass


def main():
    """
    @rtype : none
    """
    init_db_with_items()
    app = webapp2.WSGIApplication([('/', LoginPage), ('/ourproducts', MyProductPage), ('/addcart', MyCartPage)], debug=True)


if __init__=='__main__':
    main()
    