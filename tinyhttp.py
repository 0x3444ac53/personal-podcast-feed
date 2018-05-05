#!/usr/bin/env python

import SimpleHTTPServer
import SocketServer

PORT = 80

try:
   Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
   httpd = SocketServer.TCPServer(("", PORT), Handler)
   print("serving at port %d" % (PORT))
   print("Type Ctrl+C to quit")
   httpd.serve_forever()

except KeyboardInterrupt as e:
  print("\nserver stopped\nBye...") 

