# -*- coding: utf-8 -*-
# this file is released under public domain and you can use without limitations

#########################################################################
## This is a sample controller
## - index is the default action of any application
## - user is required for authentication and authorization
## - download is for downloading files uploaded in the db (does streaming)
#########################################################################
@auth.requires_login()
def index():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Welcome to IIIT Hostel")
    login_id = session.auth.user.id
    query=(db.USER_PROFILE.USER_ID == login_id)
    count = db(query).count()
    if count == 0 :
        db.USER_PROFILE.USER_ID.default=login_id
        form = SQLFORM(db.USER_PROFILE,readonly=True,showid=False,labels={'USER_ID':'User Name'})
    else:
        row = db(query).select().first()
        value = row.id
        form = SQLFORM(db.USER_PROFILE,record=db.USER_PROFILE[value],showid=False,readonly=True)
    return dict(form=form)

def bakul():
    response.flash = T("Welcome to IIIT Hostel- Bakul")
    hostel_id = 2
    query = ( (db.HOSTEL_ADMIN.USER_ID == db.auth_user.id) & 
            (db.auth_user.id == db.USER_PROFILE.USER_ID) &
            (db.HOSTEL_ADMIN.HOSTEL_ID == hostel_id ))
    fields = (db.USER_PROFILE.USER_ID,db.HOSTEL_ADMIN.DESIGNATION,db.auth_user.email,db.USER_PROFILE.PHONE)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.USER_PROFILE.USER_ID)))]
    grid2 = SQLFORM.grid(query, maxtextlength = 60,deletable=False,editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields,links=links,search_widget='',headers={'USER_PROFILE.USER_ID':'User Name'})
    return locals()

def obh():
    hostel_id = 1
    response.flash = T("Welcome to IIIT Hostel- Old Boys Hostel")
    query = ( (db.HOSTEL_ADMIN.USER_ID == db.auth_user.id) & 
            (db.auth_user.id == db.USER_PROFILE.USER_ID) &
            (db.HOSTEL_ADMIN.HOSTEL_ID == hostel_id ))
    fields = (db.USER_PROFILE.USER_ID,db.HOSTEL_ADMIN.DESIGNATION,db.auth_user.email,db.USER_PROFILE.PHONE)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.USER_PROFILE.USER_ID)))]
    grid2 = SQLFORM.grid(query, maxtextlength = 60,deletable=False,editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields,links=links,search_widget='',headers={'USER_PROFILE.USER_ID':'User Name'})
    return locals()

def nbh():
    response.flash = T("Welcome to IIIT Hostel- New Boys Hostel")
    hostel_id = 3
    query = ( (db.HOSTEL_ADMIN.USER_ID == db.auth_user.id) & 
            (db.auth_user.id == db.USER_PROFILE.USER_ID) &
            (db.HOSTEL_ADMIN.HOSTEL_ID == hostel_id ))
    fields = (db.USER_PROFILE.USER_ID,db.HOSTEL_ADMIN.DESIGNATION,db.auth_user.email,db.USER_PROFILE.PHONE)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.USER_PROFILE.USER_ID)))]
    grid2 = SQLFORM.grid(query, maxtextlength = 60,deletable=False,editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields,links=links,search_widget='',headers={'USER_PROFILE.USER_ID':'User Name'})
    return locals()

def parijat():
    response.flash = T("Welcome to IIIT Hostel- Parijat")
    hostel_id = 4
    query = ( (db.HOSTEL_ADMIN.USER_ID == db.auth_user.id) & 
            (db.auth_user.id == db.USER_PROFILE.USER_ID) &
            (db.HOSTEL_ADMIN.HOSTEL_ID == hostel_id ))
    fields = (db.USER_PROFILE.USER_ID,db.HOSTEL_ADMIN.DESIGNATION,db.auth_user.email,db.USER_PROFILE.PHONE)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.USER_PROFILE.USER_ID)))]
    grid2 = SQLFORM.grid(query, maxtextlength = 60,deletable=False,editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields,links=links,search_widget='',headers={'USER_PROFILE.USER_ID':'User Name'})
    return locals()

def index2():
    """
    example action using the internationalization operator T and flash
    rendered by views/default/index.html or views/generic.html

    if you need a simple wiki simply replace the two lines below with:
    return auth.wiki()
    """
    response.flash = T("Hello World")
    return dict(message=T('Welcome to web2py!'))


def user():
    """
    exposes:
    http://..../[app]/default/user/login
    http://..../[app]/default/user/logout
    http://..../[app]/default/user/register
    http://..../[app]/default/user/profile
    http://..../[app]/default/user/retrieve_password
    http://..../[app]/default/user/change_password
    http://..../[app]/default/user/manage_users (requires membership in
    http://..../[app]/default/user/bulk_register
    use @auth.requires_login()
        @auth.requires_membership('group name')
        @auth.requires_permission('read','table name',record_id)
    to decorate functions that need access control
    """
    return dict(form=auth())


@cache.action()
def download():
    """
    allows downloading of uploaded files
    http://..../[app]/default/download/[filename]
    """
    return response.download(request, db)


def call():
    """
    exposes services. for example:
    http://..../[app]/default/call/jsonrpc
    decorate with @services.jsonrpc the functions to expose
    supports xml, json, xmlrpc, jsonrpc, amfrpc, rss, csv
    """
    return service()
