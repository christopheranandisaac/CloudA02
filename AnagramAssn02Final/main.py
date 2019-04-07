from itertools import groupby
import webapp2
import jinja2
from google.appengine.api import users
import os
from mylist import MyList
from google.appengine.ext import ndb


JINJA_ENVIRONMENT = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),extensions=['jinja2.ext.autoescape'],autoescape=True)

class MainPage(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        url = ''
        url_string = ''
        welcome = 'Welcome back'
        my_list = None
        a=[]
        user = users.get_current_user()
        if user:
            url = users.create_logout_url(self.request.uri)
            url_string = 'logout'
            key = ndb.Key('MyList', user.user_id())
            email=users.get_current_user().email()
            string = self.request.get('input77')
            string7=''.join(k for k, g in groupby(sorted(string)))
            query=MyList.query(MyList.email==users.get_current_user().email())

            string8=None
            my_list1=None
            for i in query:
                if i.lexographical in string7:
                    if i.lexographical==string7:
                        pass
                    else:
                        string8=i.lexographical
                        if string8==None:
                            pass
                        else:
                            key1=ndb.Key('MyList',string8+email)
                            my_list1=key1.get()
                            a.append(my_list1)
            key = ndb.Key('MyList', string7+email)
            my_list = key.get()
        else:
            url = users.create_login_url(self.request.uri)
            url_string = 'login'
        template_values = {'url' : url,'url_string' : url_string,'user' : user,'welcome' : welcome,'my_list' : my_list,'my_list':my_list,'a':a}
        template = JINJA_ENVIRONMENT.get_template('main.html')
        self.response.write(template.render(template_values))

    def post(self):
            self.response.headers['Content-Type'] = 'text/html'
            user = users.get_current_user()
            string = self.request.get('input')
            string7=''.join(k for k, g in groupby(sorted(string)))
            emailsample=users.get_current_user().email()
            key = ndb.Key('MyList', string7+emailsample)
            my_list = key.get()
            if my_list==None:
                my_list=MyList(id=string7+emailsample)
                my_list.put()
            key = ndb.Key('MyList', string7+emailsample)
            my_list = key.get()
            action=self.request.get('button')
            if action == 'add':
                string = self.request.get('input')
                if string == None or string == '':
                    self.redirect('/')
                    return
                my_list.strings.append(string)
                my_list.lexographical=string7
                my_list.wordcount=len(my_list.strings)
                my_list.lettercount=len(my_list.lexographical)
                my_list.email=emailsample
            my_list.put()
            self.redirect('/add')

class AddPage(webapp2.RequestHandler):
    def get(self):
        user = users.get_current_user()
        self.response.out.write("<html><head></head><body>")
        self.response.out.write("""<form method="post" align="center" action="/"><p>
        <i>Enter the word</i>:<input type="text" name="input" pattern="[a-zA-Z]+" required="True"/><br/>
        <input type="submit" name="button" value="add"/></p>
        </form>""")
        self.response.out.write("<b><p><a href='/'><i>Home</i></a></p></b>")
        self.response.out.write("</body></html>")

# class SearchA(webapp2.RequestHandler):
#     def get(self):
#         self.response.headers['Content-Type'] = 'text/html'
#         email=users.get_current_user().email()
#         string = self.request.get('input77')
#         string7=''.join(k for k, g in groupby(sorted(string)))
#         query=MyList.query(MyList.email==users.get_current_user().email())
#         a=[]
#         string8=None
#         my_list1=None
#         for i in query:
#             if i.lexographical in string7:
#                 if i.lexographical==string7:
#                     pass
#                 else:
#                     string8=i.lexographical
#                     if string8==None:
#                         pass
#                     else:
#                         key1=ndb.Key('MyList',string8+email)
#                         my_list1=key1.get()
#                         a.append(my_list1)
#         key = ndb.Key('MyList', string7+email)
#         my_list = key.get()
#         template_values = {'my_list':my_list,'a':a}
#         template = JINJA_ENVIRONMENT.get_template('search.html')
#         self.response.write(template.render(template_values))

class UAnagram(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        user=users.get_current_user().email()
        query=MyList.query(MyList.email==users.get_current_user().email())
        template_values = {'query':query}
        template = JINJA_ENVIRONMENT.get_template('uanagram.html')
        self.response.write(template.render(template_values))

class WordList(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        template_values = {}
        template = JINJA_ENVIRONMENT.get_template('wordlist.html')
        self.response.write(template.render(template_values))

    def post(self):
        self.response.headers['Content-Type'] = 'text/html'
        user = users.get_current_user().email()
        textfile = self.request.get("myFile")
        textfile = textfile.split()
        for x in textfile:
            line=''.join(k for k, g in groupby(sorted(x)))
            key = ndb.Key('MyList', line+user)
            my_list = key.get()
            if my_list==None:
                my_list=MyList(id=line+user)
                my_list.put()
            key = ndb.Key('MyList', line+user)
            my_list = key.get()
            my_list.strings.append(x)
            my_list.lexographical=line
            my_list.wordcount=len(my_list.strings)
            my_list.lettercount=len(my_list.lexographical)
            my_list.email=user
            my_list.put()
        self.redirect('/')









app = webapp2.WSGIApplication([('/', MainPage),('/add',AddPage),('/uanagram',UAnagram),('/wordlist',WordList)], debug=True)
