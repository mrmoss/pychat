#!/usr/bin/env python2
import SimpleHTTPServer
import BaseHTTPServer
import urllib
import urlparse

history={}

class MyHandler(SimpleHTTPServer.SimpleHTTPRequestHandler):
	def do_GET(self):
		global history

		try:
			file=open('chat.ind','r')
			self.send_response(200)
			self.send_header('Content-type','text/html')
			self.end_headers()
			self.wfile.write(file.read())
			self.wfile.close()
		except Exception:
			pass
	def do_POST(self):
		global history

		try:
			query_str=urlparse.urlparse(self.path).query
			room=None

			for query in query_str.split('&'):
				try:
					query=query.split('=')

					if len(query)>1:
						key=query[0]
						val=urllib.unquote(query[1])

						if key=='room':
							room=val
							if not val in history:
								history[val]=''
						elif key=='tx':
							if room:
								data_len=int(self.headers.getheader('content-length',0))
								if data_len>100:
									data_len=100
								data=self.rfile.read(data_len)
								data.replace('\n','')
								data.replace('\r','')
								history[room]+=data+'\n'
								history[room]='\n'.join(history[room].split('\n')[-100:])
								self.send_response(200)
								self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(' ')
							self.wfile.close()
						elif key=='rx':
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							if room:
								self.wfile.write(history[room])
							self.wfile.close()
				except Exception:
					pass
		except Exception:
			pass

try:
	Handler=MyHandler
	server=BaseHTTPServer.HTTPServer(('127.0.0.1',8080),MyHandler)
	server.serve_forever()
except Exception:
	pass
