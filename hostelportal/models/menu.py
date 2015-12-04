# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## Customize your APP title, subtitle and menus here
#########################################################################

response.logo = A(B('web',SPAN(2),'py'),XML('&trade;&nbsp;'),
                  _class="navbar-brand",_href="http://www.web2py.com/",
                  _id="web2py-logo")
response.title = request.application.replace('_',' ').title()
response.subtitle = ''

## read more at http://dev.w3.org/html5/markup/meta.name.html
response.meta.author = 'Your Name <you@example.com>'
response.meta.description = 'a cool new app'
response.meta.keywords = 'web2py, python, framework'
response.meta.generator = 'Web2py Web Framework'

## your http://google.com/analytics id
response.google_analytics_id = None

#########################################################################
## this is the main application menu add/remove items as required
#########################################################################

response.menu = [
    (T('Home'), False, URL('default', 'index'), [])
]

DEVELOPMENT_MENU = True

#########################################################################
## provide shortcuts for development. remove in production
#########################################################################

def _():
    # shortcuts
    app = request.application
    ctr = request.controller
    count = 0
    if(session!= None and session.auth != None and  session.auth.user.id != None):
        login_id = session.auth.user.id
        query=(  (db.IM_MESSAGE.RECEIVER == login_id) & (db.IM_MESSAGE.SEEN == False))
        count = db(query).count()
    # useful links to internal and external resources
    response.menu += [
        ('Discussion Forum', False, URL('hostel', 'user', 'viewforum')),
        ('Complaints', False, URL('hostel', 'user', 'complaint')),
          (T('Message'), False, '#', [
              (T('Compose Message'), False, URL('hostel', 'user', 'message' )),
              LI(_class="divider"),
              (T('New Message('+str(count)+')'), False,
               URL(
               'hostel', 'user', 'newmessage' )),
              (T('Message'), False,
               URL(
               'hostel', 'user', 'viewmessage' )),
              ]),
        ('All Users', False, URL('hostel', 'user', 'users')),
        ('Edit Profile', False, URL('hostel', 'user', 'editprofile'))
        ]
if DEVELOPMENT_MENU: _()

if "auth" in locals(): auth.wikimenu()
