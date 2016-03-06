#!/usr/bin/env python
import SimpleHTTPServer
import BaseHTTPServer
import urllib
import urlparse

history=''

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
		except:
			pass
	def do_POST(self):
		global history

		try:
			query_str=urlparse.urlparse(self.path).query

			for query in query_str.split('&'):
				try:
					query=query.split('=')

					if len(query)>1:
						key=query[0]
						val=urllib.unquote(query[1])

						if key=='tx':
							data_len=int(self.headers.getheader('content-length',0))
							if data_len>100:
								data_len=100
							data=self.rfile.read(data_len)
							data.replace('\n','')
							data.replace('\r','')
							history+=data+'\n'
							history='\n'.join(history.split('\n')[-100:])
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(' ')
							self.wfile.close()
						elif key=='rx':
							self.send_response(200)
							self.send_header('Content-type','text/html')
							self.end_headers()
							self.wfile.write(history)
							self.wfile.close()
				except:
					pass
		except:
			pass

try:
	Handler=MyHandler
	server=BaseHTTPServer.HTTPServer(('127.0.0.1',8080),MyHandler)
	server.serve_forever()
except:
	pass