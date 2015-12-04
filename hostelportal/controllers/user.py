# -*- coding: utf-8 -*-
# try something like
from gluon.tools import Crud
# -*- coding: utf-8 -*-
# try something like\
@auth.requires_login()
def index():
    db.DISCUSSION_FORUMS.CREATED_ON.writable = False
    form = SQLFORM(db.DISCUSSION_FORUMS,fields=fields,submit_button='Create New Discussion Forum')
    if form.process().accepted:
        response.flash = 'New Discussion Forum Created.'
    elif form.errors:
        response.flash = 'Error exist in Discussion Forum Creation.'
    fields = (db.DISCUSSION_FORUMS.TITLE, db.DISCUSSION_FORUMS.CREATED_ON, db.DISCUSSION_FORUMS.CREATED_BY)
    links =  [lambda row: A('View Discussion Forum',_href=URL("student","viewforum.html",vars=dict(dfid=row.id)))]
    grid = SQLFORM.smartgrid(db.DISCUSSION_FORUMS,deletable=False,maxtextlength=50, editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields, links_in_grid=True,links=links,showbuttontext=True,linked_tables=False,user_signature=True,
                             search_widget='')
    return dict(rows = db(db.DISCUSSION_FORUMS).select(),form=form,grid=grid)

@auth.requires_login()
def viewforum():
    db.DISCUSSION_FORUMS.CREATED_ON.writable = False
    fields=['TITLE','DESCRIPTION']
    form = SQLFORM(db.DISCUSSION_FORUMS,fields=fields,submit_button='Create New Discussion Forum')
    if form.process().accepted:
        response.flash = 'New Discussion Forum Created.'
    elif form.errors:
        response.flash = 'Error exist in Discussion Forum Creation.'
    fields = (db.DISCUSSION_FORUMS.TITLE, db.DISCUSSION_FORUMS.CREATED_ON, db.DISCUSSION_FORUMS.CREATED_BY)
    links =  [lambda row: A('View Discussion Forum',_href=URL("user","viewparticularforum.html",vars=dict(dfid=row.id)))]
    grid = SQLFORM.smartgrid(db.DISCUSSION_FORUMS,deletable=False,maxtextlength=50, editable=False, details=False, selectable=None, create=False, csv=False
                            ,fields=fields, links_in_grid=True,links=links,showbuttontext=True,linked_tables=False,user_signature=True,
                             )
    return dict(rows = db(db.DISCUSSION_FORUMS).select(),form=form,grid=grid)

@auth.requires_login()
def viewparticularforum():
    var=request.get_vars['dfid']
    db.DISCUSSION_FORUMS_COMMENTS.DF_ID.default = var
    form = SQLFORM(db.DISCUSSION_FORUMS_COMMENTS,submit_button='Post Reply')
    if form.process().accepted:
        response.flash = 'Reply Posted'
    elif form.errors:
        response.flash = 'Reply has errors. Kindly repost.'
    row = db(db.DISCUSSION_FORUMS.id ==var ).select()
    dfform = SQLFORM(db.DISCUSSION_FORUMS,record = db.DISCUSSION_FORUMS[var],readonly=True,ignore_rw=True, showid=False,comments=True,
                    fields=['TITLE','DESCRIPTION','CREATED_ON','CREATED_BY'])
    #comments = SQLFORM(db.DISCUSSION_FORUMS_COMMENTS,record = db.DISCUSSION_FORUMS_COMMENTS(db.DISCUSSION_FORUMS_COMMENTS.DF_ID == var), 
    #                readonly=True,ignore_rw=True, showid=False,comments=True)
    comments=db( (db.DISCUSSION_FORUMS_COMMENTS.DF_ID == var) &
                (db.auth_user.id == db.DISCUSSION_FORUMS_COMMENTS.CREATED_BY )).select(db.DISCUSSION_FORUMS_COMMENTS.REPLY,
                                                                  db.DISCUSSION_FORUMS_COMMENTS.id,
                                                                  db.auth_user.first_name,db.auth_user.last_name,db.auth_user.id,
                                                                  db.DISCUSSION_FORUMS_COMMENTS.CREATED_ON)
    resDict = dict(form=form,dfform=dfform,comments=comments)
    return resDict


@auth.requires_login()
def message():
    var=request.get_vars['receiveid']
    login_id = session.auth.user.id
    responseDict = dict()
    if(var != None):
        receive_id = long(var)
        db.IM_MESSAGE.RECEIVER.default = receive_id
        db.IM_MESSAGE.RECEIVER.writeble= False
    form = SQLFORM(db.IM_MESSAGE,fields = ['SENDER','RECEIVER','MESSAGE_DETAIL'],submit_button='Send Message')
    if form.process().accepted:
        response.flash = 'Message Send'
    elif form.errors:
        response.flash = 'Message has Errors'
    responseDict['form']=form
    rows=list()
    if(var != None):
        receive_id = long(var)
        send_id = long(login_id)
        db.IM_MESSAGE.RECEIVER.default = receive_id
        db.IM_MESSAGE.RECEIVER.Writable = False
        query=( ((db.IM_MESSAGE.SENDER == send_id) & (db.IM_MESSAGE.RECEIVER == receive_id)) |
              ((db.IM_MESSAGE.SENDER == receive_id) & (db.IM_MESSAGE.RECEIVER == send_id)) )
        rows = db(query).select(orderby=~db.IM_MESSAGE.CREATED_ON)
        query1=( (db.IM_MESSAGE.RECEIVER == send_id) & (db.IM_MESSAGE.SENDER == receive_id) & (db.IM_MESSAGE.SEEN == False)) 
        rows1 = db(query1).select()
        for row in rows1:
            row.update_record(SEEN = True)
        query=(db.auth_user.id == send_id)
        row_send = db(query).select().first()
        responseDict['send_id']= send_id
        responseDict['send_name']= row_send.first_name + ' ' + row_send.last_name
        query=(db.auth_user.id == receive_id)
        row_send = db(query).select().first()
        responseDict['receive_id']= receive_id
        responseDict['receive_name']= row_send.first_name + ' ' + row_send.last_name
        responseDict['login_id']= login_id
    responseDict['rows']= rows
    return responseDict
@auth.requires_login()
def editprofile():
    ALL_BLOOD_GROUP = ('A+','B+','AB+','O+','A-','B-','AB-','O-')
    login_id = session.auth.user.id
    db.USER_PROFILE.BLOOD_GROUP.requires = IS_IN_SET(ALL_BLOOD_GROUP)
    if(login_id != None):
        query=(db.USER_PROFILE.USER_ID == login_id)
        count = db(query).count()
        if count == 0 :
            form = SQLFORM(db.USER_PROFILE,showid=False,fields=['ROLL_NUMBER','PHONE','ROOM_NUMBER','HOME_ADDRESS','ALLERGY','DATE_OF_BIRTH','BLOOD_GROUP'])
        else:
            query=(db.USER_PROFILE.USER_ID == login_id)
            row = db(query).select().first()
            form = SQLFORM(db.USER_PROFILE,record=db.USER_PROFILE[row.USER_ID],showid=False,
                          fields=['ROLL_NUMBER','PHONE','ROOM_NUMBER','HOME_ADDRESS','ALLERGY','DATE_OF_BIRTH','BLOOD_GROUP'],
                          submit_button='Update Profile')
    if form.process().accepted:
        response.flash = 'Profile Updated'
    elif form.errors:
        response.flash = 'Profile Updation Failed.'
    return dict(form=form,query=query)
@auth.requires_login()
def profile():
    ALL_BLOOD_GROUP = ('A+','B+','AB+','O+','A-','B-','AB-','O-')
    user_id = request.get_vars['userid']
    if user_id != None:
        user_id = long(user_id)
    else:
        user_id = login_id
    db.USER_PROFILE.BLOOD_GROUP.requires = IS_IN_SET(ALL_BLOOD_GROUP)
    query=(db.USER_PROFILE.USER_ID == user_id)
    count = db(query).count()
    if count == 0 :
        db.USER_PROFILE.USER_ID.default=user_id
        form = SQLFORM(db.USER_PROFILE,readonly=True,showid=False)
    else:
        row = db(query).select().first()
        value = row.id
        form = SQLFORM(db.USER_PROFILE,record=db.USER_PROFILE[value],showid=False,readonly=True)
    return dict(form=form)
@auth.requires_login()
def newmessage():
    login_id = long(session.auth.user.id)
    query=(  (db.IM_MESSAGE.RECEIVER == login_id) & (db.IM_MESSAGE.SEEN == False))
    rows = db(query).select(db.IM_MESSAGE.SENDER, distinct=True)
    fields = (db.IM_MESSAGE.SENDER, db.IM_MESSAGE.MESSAGE_DETAIL)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.SENDER))), 
              lambda row: '  ',
              lambda row: A('View Profile',_href=URL("user","profile",vars=dict(userid=row.SENDER)))]
    grid = SQLFORM.smartgrid(db.IM_MESSAGE,constraints = dict(IM_MESSAGE=query),deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,links=links,fields=fields,
                            links_in_grid=True,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.IM_MESSAGE.CREATED_ON ,
                             search_widget='')
    return dict(grid=grid)

@auth.requires_login()
def viewmessage():
    login_id = long(session.auth.user.id)
    query=(  (db.IM_MESSAGE.RECEIVER == login_id) & (db.IM_MESSAGE.SEEN == False))
    rows = db(query).select(db.IM_MESSAGE.SENDER, distinct=True)
    fields = (db.IM_MESSAGE.SENDER, db.IM_MESSAGE.MESSAGE_DETAIL)
    links =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.SENDER))), 
              lambda row: A('View Profile',_href=URL("user","profile",vars=dict(userid=row.SENDER)))]
    grid = SQLFORM.smartgrid(db.IM_MESSAGE,constraints = dict(IM_MESSAGE=query),deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,links=links,fields=fields,
                            links_in_grid=True,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.IM_MESSAGE.CREATED_ON ,
                             search_widget='')
    query1=(  (db.IM_MESSAGE.RECEIVER == login_id))
    grid1 = SQLFORM.smartgrid(db.IM_MESSAGE,constraints = dict(IM_MESSAGE=query1),deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,links=links,fields=fields,
                            links_in_grid=True,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.IM_MESSAGE.CREATED_ON ,
                             search_widget='' )
    fields2 = (db.IM_MESSAGE.RECEIVER, db.IM_MESSAGE.MESSAGE_DETAIL)
    query2=(  (db.IM_MESSAGE.SENDER== login_id))
    links2 =  [lambda row: A('View Message Thread',_href=URL("user","message",vars=dict(receiveid=row.RECEIVER))), 
              lambda row: A('View Profile',_href=URL("user","profile",vars=dict(userid=row.RECEIVER)))]
    grid2 = SQLFORM.smartgrid(db.IM_MESSAGE,constraints = dict(IM_MESSAGE=query2),deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,links=links2,fields=fields2,
                            links_in_grid=True,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.IM_MESSAGE.CREATED_ON ,
                             search_widget='' )
    return dict(grid1=grid1,grid2=grid2)

@auth.requires_login()
def complaint():
    ALL_COMPLAINT_TYPE = ('Carpenter','Electrical','Sanitary','Others')
    ALL_SLOTS = ('0000','0100','0200','0300','0400','0500','0600','0700','0800','0900','1000','1100','1200','1300',
                 '1400','1500','1600','1700','1800','1900','2000','2100','2200','2300')
    login_id = session.auth.user.id
    db.COMPLAINT.COMPLAINT_TYPE.requires = IS_IN_SET(ALL_COMPLAINT_TYPE)
    db.COMPLAINT.AVALIABLE_SLOT_FROM.requires = IS_IN_SET(ALL_SLOTS)
    db.COMPLAINT.AVALIABLE_SLOT_TO.requires = IS_IN_SET(ALL_SLOTS)
    form = SQLFORM(db.COMPLAINT,fields = ['COMPLAINT_TYPE','YOUR_COMPLAINT','AVALIABLE_SLOT_FROM','AVALIABLE_SLOT_TO']
                  ,submit_button='Create New Complaint')
    if form.process().accepted:
        response.flash = 'Complaint Noted'
    elif form.errors:
        response.flash = 'Complaint Notion Failed.'
    query=(db.COMPLAINT.CREATED_BY == login_id)
    fields = (db.COMPLAINT.COMPLAINT_TYPE, db.COMPLAINT.YOUR_COMPLAINT,db.COMPLAINT.AVALIABLE_SLOT_FROM,db.COMPLAINT.AVALIABLE_SLOT_TO)
    grid1 = SQLFORM.smartgrid(db.COMPLAINT,constraints = dict(COMPLAINT=query),deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,fields=fields,
                            links_in_grid=False,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.COMPLAINT.CREATED_ON ,
                             search_widget='')
    gridall = None
    login_id = session.auth.user.id
    query=(db.HOSTEL_ADMIN.USER_ID == login_id)
    count = db(query).count()
    if count > 0 :
        gridall = SQLFORM.smartgrid(db.COMPLAINT,deletable=False,maxtextlength=50, editable=False, 
                             details=False, selectable=None, create=False, csv=False,fields=fields,
                            links_in_grid=False,showbuttontext=True,linked_tables=False,user_signature=True,orderby=~db.COMPLAINT.CREATED_ON ,
                             search_widget='')
    return locals()

@auth.requires_login()
def users():
    links =  [lambda row: A('Start Message Thread',_href=URL("user","message",vars=dict(receiveid=row.USER_ID)))]
    fields = (db.USER_PROFILE.USER_ID, db.USER_PROFILE.ROLL_NUMBER,
              db.USER_PROFILE.PHONE,db.USER_PROFILE.ROOM_NUMBER,db.USER_PROFILE.HOME_ADDRESS,db.USER_PROFILE.ALLERGY,
              db.USER_PROFILE.DATE_OF_BIRTH,db.USER_PROFILE.BLOOD_GROUP)
    grid1 = SQLFORM.smartgrid(db.USER_PROFILE ,deletable=False,maxtextlength=50, editable=False,fields=fields
                             ,details=False, selectable=None, create=False, csv=False,links=links,
                            links_in_grid=True,showbuttontext=True,linked_tables=False,user_signature=True,
                              headers={'USER_PROFILE.USER_ID':'User Name'}
                             )
    return locals()
