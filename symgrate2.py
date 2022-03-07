import http.client as httplib
import urllib.parse
import json


"""A Python3 library for the Symgrate web API."""

global SEARCHLEN
SEARCHLEN=18

class symgrate:
    def __init__(self, URL="symgrate.com",port=80):
        self.URL = URL
        self.port = port
        self.conn = httplib.HTTPConnection(URL,port)
        self.headers = {"Content-type": "application/x-www-form-urlencoded", "Accept": "text/plain"}

    def jprint(self,j):
        """Prints the results from JSON."""
        # Parse the JSON.
        x=json.loads(j)

        #Print each name and record.
        for f in x:
            #print(f, x[f]["Name"])
            print(f)

    def close(self):
        self.conn.close()

    def do_query(self,api_str,q):
        params=q
        try:
            params = urllib.parse.urlencode(q)
        except TypeError:
            pass;

        #print("querying API %s with params: %s" %(api_str,q))
        # FIXME, we should be taking bytes as raw instead of a string.
        self.conn.request("POST", api_str, params, self.headers)
        
        r1 = self.conn.getresponse()
        #print r1.status, r1.reason
        # 200 OK ?
        toret=None
        if r1.status==200:
            data = r1.read()
            if len(data)>2:
                toret=data.decode("utf-8")
        else:
            print("connection status: %d" % r1.status)

        # TODO: This would go a little faster if we reused the socket.
        self.close()
        return toret

    #qlist is an array of (a,b) pairs    
    def format_list(self,qlist):
        qstr = ""
        for i in range(len(qlist)):
            (a,b) = qlist[i]
            qstr+="%s=%s&"%(a,b)
        return qstr

    #API queries
    #each param is a list of pairs depending on the API
    #we'll format them up into a string query (format_list) and send it over (do_query)

    #Params
    #jfns - (addr, hex string of first 18 bytes)
    #jsvd - (chip name, chip name)
    #jregs - (addr, type of access ('r','w','u'))

    def queryjfns(self,qlist):
        return self.do_query("/jfns",self.format_list(qlist))

    def queryjsvd(self,qlist):
        return self.do_query("/jsvd",self.format_list(qlist))

    def queryjregs(self,qlist):
        return self.do_query("/jregs",self.format_list(qlist))

