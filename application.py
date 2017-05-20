import urllib.request
import json

def application(environ, start_response):
	requestmethod=environ['SCRIPT_NAME'][1:]
	requesturi=environ['PATH_INFO'][1:]
	if requestmethod or requesturi:
		parsedqs=urllib.parse.parse_qs(environ['QUERY_STRING'])
		#urllib.unquote
		with urllib.request.urlopen(urllib.request.Request(parsedqs['uri'][0],headers={'User-Agent':'Mozilla/5.0'},method=parsedqs['method'][0])) as httpresp:
			itemlst=httpresp.getheaders()
			itemlst.insert(0,('Status code',httpresp.status))
			#respbody=httpresp.read()
			#start_response('200 OK', [('Content-Type', 'text/html')])
			#yield respbody
			#if respbody:
			if parsedqs['method'][0] == 'GET':
				respbody=httpresp.read()
				itemlst.append(('Body',respbody.decode("utf-8")))#//todo parse charset from content-type?
			start_response('200 OK', [('Content-Type', 'application/json')])
			yield json.dumps(itemlst)
	else:
		start_response('200 OK', [('Content-Type', 'text/html')])
		#start_response('404 Not Found', [('Content-Type', 'text/plain')])
		with open('index.htm','r') as htmlf:
			yield htmlf.read()
		#yield #'Hello World\n'
