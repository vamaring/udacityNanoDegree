import os
import webapp2
import jinja2

template_dir = os.path.join(os.path.dirname(__file__),'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir),
							   autoescape = True)

def render_str(template, **params):
	t = jinja_env.get_template(template)
	return t.render(params)
		
class BaseHandler(webapp2.RequestHandler):
	def write(self, *a, **kw):
		self.response.out.write(*a, **kw)
				
	def display(self, template, **kw):
		self.response.out.write(render_str(template,**kw))
		
class Rot13Handler(BaseHandler):
	def get(self):
		self.display('rot13-form.html')
	
	def post(self):
		rot13 = ''
		text = self.request.get('text')
		if text:
			rot13 = text.encode('rot13')
		
		self.display('rot13-form.html', text = rot13)
		
app = webapp2.WSGIApplication([('/unit2/rot13', Rot13Handler)],debug = True)