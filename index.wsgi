import os

def application(env, start_response):
    start_response('200 OK', [('Content-Type','text/html')])

    fpath = os.path.join(os.path.dirname(os.path.realpath(__file__)), "index.html")
    with open(fpath, "r") as f:
      content = []
      for line in f:
        content.append(line)	  
    return content

