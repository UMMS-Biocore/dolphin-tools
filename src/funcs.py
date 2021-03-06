#!/usr/bin/python
import logging
import urllib,urllib2
import json
import os
import re
import cgi
import warnings
import sys
import time

class funcs:
    re_string = re.compile(r'(?P<htmlchars>[<&>])|(?P<space>^[ \t]+)|(?P<lineend>\r\n|\r|\n)|(?P<protocal>(^|\s)((http|ftp)://.*?))(\s|$)', re.S|re.M|re.I)

    def plaintext2html(self, text, tabstop=4):
        def do_sub(m):
            c = m.groupdict()
            if c['htmlchars']:
                return cgi.escape(c['htmlchars'])
            if c['lineend']:
                return '<br>'
            elif c['space']:
                t = m.group().replace('\t', '&nbsp;'*tabstop)
                t = t.replace(' ', '&nbsp;')
                return t
            elif c['space'] == '\t':
                return ' '*tabstop;
            else:
                url = m.group('protocal')
                if url.startswith(' '):
                    prefix = ' '
                    url = url[1:]
                else:
                    prefix = ''
                last = m.groups()[-1]
                if last in ['\n', '\r', '\r\n']:
                    last = '<br>'
                return '%s<a href="%s">%s</a>%s' % (prefix, url, url, last)
        return re.sub(self.re_string, do_sub, text)
    
    def getCommand(self,argv):
       cmd=""
       for arg in sys.argv:
          arg = ( "\\\""+arg+"\\\"" if " " in arg else arg )
          cmd=cmd + str(arg) + " "
       return cmd
          
    def queryAPI(self, url, data, name=None, logging=None):
        print ("DATA:"+str(data))
        if logging:
           logging.info("DATA:"+str(data))
        opener = urllib2.build_opener(urllib2.HTTPHandler())
        trials=0
        ret = ""
        while trials<5:
           try:
              mesg = opener.open(url, data=data).read()
              ret=str(json.loads(mesg))
              ret = re.sub (r'u\'', '\'', ret)
              ret = re.sub (r'\'', '\"', ret)
              print("RESULT[%s]:[%s]"%(str(trials), str(mesg)) )
              if logging:
                  logging.info("RESULT[%s]:[%s]"%(str(trials), str(mesg)) )
              if mesg:
                 trials=5
           except:
              print "Couldn't connect to dolphin server (%s)"%trials
              if logging:
                 logging.info("Couldn't connect to dolphin server (%s)"%trials)
              time.sleep(5)
           trials=trials+1
        if logging and name: 
           logging.info("%s:%s"%(name,ret))
    
        if (ret.startswith("ERROR")):
              if logging:
                 logging.info("%s:%s"%(name,ret))
              if name:
                 print name + ":" + ret + "\n"
              sys.exit(2);
        return ret
    # error
    def stop_err(self, msg ):
        sys.stderr.write( "%s\n" % msg )
        sys.exit(2)

def main():

   try:
      print "HERE" 
   except:
      sys.exit(2)

if __name__ == "__main__":
    main()
