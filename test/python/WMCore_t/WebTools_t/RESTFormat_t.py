#!/usr/bin/env python
"""
_REST_t_

Unit tests for checking RESTModel works correctly

TODO: duplicate all direct call tests to ones that use HTTP
"""

__revision__ = "$Id: RESTFormat_t.py,v 1.6 2010/01/14 22:20:08 sryu Exp $"
__version__ = "$Revision: 1.6 $"

import unittest
import json
import urllib

from cherrypy import HTTPError
from WMCore.WebTools.RESTFormatter import RESTFormatter
from DummyRESTModel import DummyRESTModel

from WMQuality.WebTools.RESTBaseUnitTest import RESTBaseUnitTest
from WMQuality.WebTools.RESTClientAPI import methodTest
from WMQuality.WebTools.RESTServerSetup import DefaultConfig

class RESTFormatTest(RESTBaseUnitTest):
    
    def initialize(self):
        self.config = DefaultConfig('DummyRESTModel')        
        self.urlbase = self.config.getServerUrl()
    
    def testUnsupportedFormat(self):
        
        # test not accepted type should return 406 error
        url = self.urlbase +'list1/'
        methodTest('GET', url, accept='text/das', output={'code':406})
    
    def testSupportedFormat(self):
    
        rf = RESTFormatter(config=self.config.Webtools)
        url = self.urlbase +'list1/'
        
        for type in rf.supporttypes.keys():
            # test accepted type should return 200 error
            methodTest('GET', url, accept=type, output={'code':200})
    
    def testEncodedInput(self):
        
        type = 'text/plain'
       
        url = self.urlbase + 'list3?a=a%&b=b'
        print url
        methodTest('GET', url, accept=type, 
                         output={'code':200, 'data':"{'a': 'a%', 'b': 'b'}"})
       
        input={'a':'%', 'b':'b'}  
           
        #methodTest encoded input with urlencode
        url = self.urlbase +'list3'
        methodTest('GET', url, accept=type, input=input, 
                         output={'code':200, 'data':"{'a': '%', 'b': 'b'}"})
        
        
        # fix this
#        methodTest('POST', '/rest/list3', accept=type, input=input,
#                         contentType="application/json",
#                         output={'code':200, 'data':"{'a': '%', 'b': 'b'}"}
#                         )
        
        input={'a':'%', 'b':'b'}
        url = self.urlbase +'list3'  
        methodTest('POST', url, accept=type, input=input,
                         output={'code':200, 'data':"{'a': '%', 'b': 'b'}"}
                         )
    
    def testReturnFormat(self):
        
        type = 'application/json'
        
        url = self.urlbase +'list3?a=a%&b=b'
        methodTest('GET', url, accept=type, 
                         output={'code':200, 'data':'{"a": "a%", "b": "b"}'})
       
        url = self.urlbase + 'list1?int=a'
        try:
            urllib.urlopen(url)
            #urllib2.urlopen(url)
        except urllib2.HTTPError, h:
            print "Exception got cought %s" % h.read()
            
        methodTest('GET', url, accept=type, 
                         output={'code':400, 
                                 'data':"""{"exception": 400, "type": "HTTPError", "message": "list1() got an unexpected keyword argument 'int'"}"""})
        url = self.urlbase + 'list?int=a&str=a'
        methodTest('GET', url, accept=type,
                         output={'code':400, 
                                 'data':"""{"exception": 400, "type": "HTTPError", "message": {"AssertionError": "val_1 failed: <type 'str'> not int"}}"""})
       
    def testException(self):
        
        import urllib2
        url = self.urlbase + 'list1?int=a'
        self.assertRaises(urllib2.HTTPError, urllib2.urlopen, url)
        
        #TODO check urllib.open is raising HTTPError
        #import urllib
        #self.assertRaises(urllib2.HTTPError, urllib.urlopen, url)
        
if __name__ == "__main__":
    unittest.main() 
        