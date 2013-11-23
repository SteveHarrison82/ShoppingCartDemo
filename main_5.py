__author__ = 'ramr'
import sys
sys.path.append("/usr/lib/python2.7/dist-packages")
sys.path.append("/home/ramakrishnan/google_appengine/lib/webapp2-2.5.2")
import cgi;
import wsgiref.handlers
import random
import os
import jinja2
import webapp2
from google.appengine.ext import db
import logging




template_dir = os.path.join(os.path.dirname(__file__),'templates')
'''template_dir variable is current dirname joined with folder name templates'''

myTemplateFolder=jinja2.FileSystemLoader(template_dir)
'''
The loader takes the path to the templates as string, or if multiple locations are wanted
a list of them which is then looked up in the given order:
>>> loader = FileSystemLoader('/path/to/templates')
>>> loader = FileSystemLoader(['/path/to/templates', '/other/path'])
'''

jinja_env = jinja2.Environment(loader = myTemplateFolder , autoescape=True)

'''
self.response.out.write(myform %{"error":error}) accepts input as string
'''

'''render_str = render string from my template folder'''




class StoreCredentialsModel(db.Model):
    UserID=db.StringProperty(required=True)
    Password=db.StringProperty(required=True)


class CartedProductModel(db.Model):
    User_with_Cart=db.ReferenceProperty(StoreCredentialsModel)
    Carted_Sku=db.StringProperty(required=True)
    Quantity_carted=db.IntegerProperty(required=True)


class AvailableProductsCatalogModel(db.Model):
    Product_Name=db.StringProperty(required=True)
    Sku_Number=db.StringProperty(required=True)
    Price=db.StringProperty(required=True)
    Product_image_url=db.StringProperty(required=False)
    Product_Attribute=db.StringProperty(required=True)

def init_db_with_product():
    """

    @rtype : return None
    """
    if (db.Query(AvailableProductsCatalogModel).count())==0:
        Addproduct1=AvailableProductsCatalogModel(Product_Name='RamaDE',
        Sku_Number='rama_1',
        Price='25e-dollar',
        Product_image_url='/images/butter/rama-de.jpeg',
        Product_Attribute='25g butter')
        Addproduct1.put()

        Addproduct2=AvailableProductsCatalogModel(Product_Name='RamaAT',
        Sku_Number='rama_2',
        Price='20e-dollar',
        Product_image_url='/images/butter/rama-at.jpeg',
        Product_Attribute='30g butter')
        Addproduct2.put()

        Addproduct3=AvailableProductsCatalogModel(Product_Name='Rama-Classic',
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
        self.response.out.write(self.request)
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
            print 'hi'
            if customerUserid and customerPwd and customerRepeatPwd !=None:
                if customerPwd == customerRepeatPwd:
                    CheckNewUserExist=StoreCredentialsModel.gql("WHERE UserID = :1", customerUserid).fetch(1)
                    if CheckNewUserExist.count(1) ==0:
                        a=StoreCredentialsModel(UserID=customerUserid, Password=customerPwd)
                        a.put()
                        mysession=str(mysession)+'-'+str(customerUserid)
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
            verifylogincredential=db.GqlQuery('select *  from  StoreCredentialsModel')

            for result in verifylogincredential:
                print result.UserID,result.Password

            verifylogincredential2=StoreCredentialsModel.gql("WHERE UserID = :1 and Password=:2", theuser, thepass)
            for result2 in verifylogincredential2:
                if result2.Password==thepass:
                    mysession=str(mysession)+'-'+theuser
                    self.response.headers.add_header('Set-Cookie', 'session='+str(mysession)+ '; Path=/')
                    self.redirect('/ourproducts')

            errorlogin="UserID or Password is wrong"
            self.response.headers.add_header('Set-Cookie', 'session='+str(mysession) +'; Path=/')
            self.render_front( error1='', error2='',errorlogin=errorlogin, userid='')


class ProducttoCartPage(Handler):
    def render_product(self,productdisplaypage=''):
        self.render_output("ProductDisplayPage.html",productdisplaypage=productdisplaypage)

    def get(self):

        mysession=self.request.cookies.get('session','0')
        productdisplaypage=db.GqlQuery('select * from  AvailableProductsCatalogModel')
        #print producttodisplay
        self.response.headers.add_header('Set-Cookie', 'session='+str(mysession)+'; Path=/')
        logging.info(u'I am on PDP')
        self.render_product(productdisplaypage)

    def get_current_user(self,UserIDfromCookie):
        #print UserIDfromCookie
        CurrentUserExist=StoreCredentialsModel.gql("WHERE UserID = :1", UserIDfromCookie).get()
        return CurrentUserExist

    def post(self):
        #self.response.out.write(self.request)
        GetSkuNumber=self.request.get('buynow')
        logging.debug( u'This is a debug message' )
        logging.info( u'This is an info message %s',GetSkuNumber )
        logging.warning( u'This is a warning' )
        logging.error( u'This is an error message' )
        logging.critical( u'FATAL!!!' )
        #self.response.out.write("the user is")
        mysession=self.request.cookies.get('session','0')
        UserIDfromCookie=str(mysession).split('-',1)[1]
        p=self.get_current_user(UserIDfromCookie)
        if p !=None:
            k=CartedProductModel(User_with_Cart=p,Carted_Sku=GetSkuNumber,Quantity_carted=1)
            k.put()
            self.redirect('/itemscarted')
        else:
            self.response.out.write("There is some problem with your cart")


class MyCartPage(Handler):

    def get_current_user(self,UserIDfromCookie):
        #print UserIDfromCookie
        CurrentUserExist=StoreCredentialsModel.gql("WHERE UserID = :1", UserIDfromCookie).get()
        return CurrentUserExist
    def get(self):
        #self.response.out.write("You are here")
        mysession=self.request.cookies.get('session','0')
        UserIDfromCookie=str(mysession).split('-',1)[1]
        p=self.get_current_user(UserIDfromCookie)
        users_cart=CartedProductModel.all()
        #self.response.out.write(users_cart)
        for each_item in users_cart:
            if each_item.User_with_Cart.UserID==UserIDfromCookie:
                self.response.out.write("True")





init_db_with_product()
app=webapp2.WSGIApplication([('/', LoginPage), ('/ourproducts', ProducttoCartPage), ('/itemscarted', MyCartPage)], debug=True)


