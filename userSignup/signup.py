import os
import webapp2
import jinja2
import re

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")
PASSWORD_RE = re.compile(r"^.{3,20}$")
EMAIL_RE = re.compile(r"^[\S]+@[\S]+.[\S]+$")

def valid_username(username):
	if username:
		return USER_RE.match(username)

def valid_password(password):
	if password:
		return PASSWORD_RE.match(password)
	
def valid_email(email):
	return not email or EMAIL_RE.match(email)
		

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)
		
class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
				
	def display(self, template, **kw):
		self.response.out.write(render_str(template,**kw))
		
class signupHandler(BaseHandler):
	def get(self):
		self.display('signup-form.html')
	
	def post(self):
		have_error = False
		username = self.request.get("username")
		password = self.request.get("password")
		verify = self.request.get("verify")
		email = self.request.get("email")
		
		params = dict(username = username, 
					  email = email)
					
		if not valid_username(username):
			params['error_username'] = "That's not a valid username"
			have_error = True
			
		if not valid_password(password):
			params['error_password'] = "That wasn't a valid password"
			have_error = True
			
		elif password != verify:
			params['error_verify'] = "Your passwords didn't match"
			have_error = True
			
		if not valid_email(email):
			params['error_email'] = "That's not a valid email"
			have_error = True
		
		if have_error:
			self.display('signup-form.html', **params)
		else:
			self.redirect('/unit2/welcome?username=' +username)
		
class welcomeHandler(BaseHandler):
	def get(self):
		username = self.request.get("username")
		if valid_username(username):
			self.display('welcome.html', username = username)
		else:
			self.redirect('/unit2/signup')
			
			
app = webapp2.WSGIApplication([('/unit2/signup', signupHandler),
							   ('/unit2/welcome', welcomeHandler)],
							   debug = True)