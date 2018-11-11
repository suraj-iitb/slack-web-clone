from django.shortcuts import render
from django.http import HttpResponse
from users.models import users
from users import views
from workspace.models import workspace, Channel, oneo1
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
import uuid
import json
import asyncio
import smtplib
# Create your views here.
loggedInUser = ""
loggedInEmail = ""
def create(request):
    # Identify which user is logged In using request.session
    # Ask user the relevant details

    # Create a workspace entry with the logged in user in Users(initially) and use the field isAdmin in JSON to denote
    # whether the user is admin or not. Set this to true for
    # the user creating the workspace

    # Do not create any channels(i.e. Set the channel field to None)

    if request.method == 'POST':
        # Issue: if workspace with same name exists it still creates that workspace
        # Issue: If user not logged in it will give error
        name = request.POST.get('workspace_name')
        userid = request.session['userid']
        username = request.session['email']

        users = {'data': [{'user_id': userid, 'email': username, 'isAdmin':True}]}
        channels = {'data':[]}
        users_json = json.dumps(users)
        channels_json = json.dumps(channels)

        work = workspace(workspace_name=name, users=users_json, channels=channels_json)
        work.save()

        views.append_workspace(userid, work.id, work.workspace_name, work.channels)

        return views.send_data(request)

    else:
        return render(request, 'create.html', {})

def is_user_admin(workid, userid):
    work = workspace.objects.get(id=int(workid))
    print(work)
    print(workid)
    print(userid)
    print(work.users)
    user_info = work.users
    print(user_info)
    user_json = json.loads(user_info)

    for data in user_json['data']:
        print(data)
        if int(data['user_id']) == int(userid):
            return True
    return False

def oneexists(request, userid):
    try:
        userc = ""
        if int(request.session['userid']) < int(userid):
            userc = userc + str(request.session['userid']) + str(userid)
        else:
            userc = userc + str(userid) +  str(request.session['userid'])
        one = oneo1.objects.get(useroneo=userc,usertwoo='')

        return True
    except:
        return False

def render_one(request, userid):
    userc = ""
    if int(request.session['userid']) < int(userid):
        userc = userc + str(request.session['userid']) + str(userid)
    else:
        userc = userc + str(userid) +  str(request.session['userid'])
    one = oneo1.objects.get(useroneo=userc,usertwoo='')
    one_messages = one.messages
    mess = []
    for data in json.loads(one_messages)['data']:
        mess.append([data['author'], data['message']])
    cont = {
        'id': one.useroneo,
        'messages':mess,
    }
    return render(request, 'oneone.html',context=cont)

def one_Create(request, userid):
    if oneexists(request, userid):
        return render_one(request, userid)
    userc = ""
    if int(request.session['userid']) < int(userid):
        userc = userc + str(request.session['userid']) + str(userid)
    else:
        userc = userc + str(userid) +  str(request.session['userid'])
    one = oneo1(useroneo=userc, usertwoo='', messages=json.dumps({'data':[]}))
    one.save()
    return render_one(request, userid)

def get_random_password():
    random = str(uuid.uuid4()) # Convert UUID format to a Python string.
    random = random.upper() # Make all characters uppercase.
    random = random.replace("-","") # Remove the UUID '-'.
    return random[0:6]

def accept_invite(request, emailid, workid, passw):
    views.create_user(emailid, passw, workid)
    work = {'data':[]}
    user = User.objects.create_user(emailid,emailid,passw)
    print("user: " + str(user))
    user.save()
    user_id = users.objects.get(email=emailid).id
    workspa = workspace.objects.get(id=workid)
    work_users = workspa.users
    work_users = json.loads(work_users)
    work_users['data'].append({'user_id':user_id, 'email':emailid, 'isAdmin': False})
    workspa.users = json.dumps(work_users)
    workspa.save()
    return show_workspace(request, workid)
def send_mail_dec(subject, message, email_from, rec_list):
    # send_mail(subject, message, email_from, rec_list)
    smtpob = smtplib.SMTP('smtp.gmail.com:587')
    smtpob.starttls()
    smtpob.login('slack.sl.iitb@gmail.com', 'IITBSLACK')
    smtpob.sendmail(email_from, rec_list, message)
    smtpob.quit()


def invite_workspace(request, workid):
    user = request.session['userid']
    if request.method == 'POST':

        if is_user_admin(workid, user):
            # replace this with send_mail
            # views.create_user(request.POST['email'], "password", workid)
            # work = {'data':[]}
            # user = User.objects.create_user(request.POST.get('email'),request.POST.get('email'),'password')
            # print("user: " + str(user))
            # user.save()
            # user_id = users.objects.get(email=request.POST.get('email')).id
            # workspa = workspace.objects.get(id=workid)
            # work_users = workspa.users
            # work_users = json.loads(work_users)
            # work_users['data'].append({'user_id':user_id, 'email':request.POST.get('email'), 'isAdmin': False})
            # workspa.users = json.dumps(work_users)
            # workspa.save()

            subject = 'Slack : Invited to a Workspace'
            message = 'You have been invited to the following workspace. Click the link below to accept\n'
            message = message + 'http://127.0.0.1:8000/workspace/accept/' + request.POST['email'] + "/" + workid + "/"+get_random_password() +'\n'

            email_from = settings.EMAIL_HOST_USER

            recipient_list = [request.POST.get('email')]
            print(recipient_list)
            send_mail_dec(subject, message, email_from, recipient_list)

            return show_workspace(request, workid)
        else:
            return HttpResponse("<h1>You are not admin to this workspace</h1>")
    else:
        return render(request, 'invite.html', {'workid': workid})
def show_workspace(request, workspace_id):
    workspaces = workspace.objects.get(id=int(workspace_id))
    workspace_channel = workspaces.channels
    workspace_channel_json = json.loads(workspace_channel)
    print(type(workspace_channel_json))
    channels = []
    for data in workspace_channel_json['data']:
        channels.append([data['name'], data['id']])
    isadmin = is_user_admin(workspace_id, int(request.session['userid']))
    print(isadmin)
    u = []
    wok = json.loads(workspaces.users)['data']
    print(wok)
    for data in wok:
        u.append([data['user_id'], data['email']])
    print(u)
    cont =  {
        'channels': channels,
        'workid': workspace_id,
        'users': u,
        'isadmin': isadmin,
    }
    return render(request, 'workspace.html', context=cont)
def create_channel(request, work_id):
    if request.method == 'POST':
        name = request.POST['workspace_name']
        user = request.session['userid']
        email = request.session['email']
        user_info = {'data': [{'id':user, 'email':email, 'isAdmin':True}]}
        messages = {'data':[]}
        channel = Channel(channel_name=name,users=json.dumps(user_info), messages=json.dumps(messages))
        channel.save()
        workspaces = workspace.objects.get(id=int(work_id))
        workspace_channel = workspaces.channels
        workspace_channel_json = json.loads(workspace_channel)
        channel_info = {'id': channel.id, 'name':channel.channel_name}
        workspace_channel_json['data'].append(channel_info)

        workspaces.channels = json.dumps(workspace_channel_json)

        workspaces.save()
        views.insert_channel(work_id, user,channel.id, name)
        return show_workspace(request, work_id)
    else:
        return render(request, 'create_channel.html', {'workid':work_id})

def channel_exists_user(user, channel_id):
    channel = Channel.objects.get(id=channel_id)
    user_info = channel.users
    user_json = json.loads(user_info)
    for data in user_json['data']:
        if int(data['id']) == user:
            return True
    return False

def render_messages(request, channel_id):
    channel = Channel.objects.get(id=channel_id)
    message = channel.messages
    message = json.loads(message)
    messages = []
    for data in message['data']:
        messages.append([data['id'],data['email'],data['message'],data['replies']])
    cont = {
        'messages': messages,
        'id': channel_id,
        'last_id': get_message_id(channel_id),
    }
    print(messages)
    return render(request, 'channel.html', context=cont)

def delete_message(mess_id, user, roomName):
    channel = Channel.objects.get(id=roomName)
    mess = channel.messages
    mess = json.loads(mess)
    for i in range(len(mess['data'])):
        if mess['data'][i]['id'] == int(mess_id):
            del mess['data'][i]
            break
    channel.messages = json.dumps(mess)
    channel.save()

def get_message_id(channel_id):
    channel = Channel.objects.get(id=channel_id)
    mess = channel.messages
    mess_json = json.loads(mess)
    if len(mess_json['data']) == 0:
        return 1
    return int(mess_json['data'][len(mess_json['data'])-1]['id']+1)


def save_reply(channelid, messageid, message):
    ch = Channel.objects.get(id=channelid)
    i = 0;
    repli_data = json.loads(ch.messages)['data']

    for data in repli_data:

        if data['id'] == int(messageid):
            #rep_json = json.loads(data)
            break
        i = i+1

    mess = ch.messages
    mess_json = json.loads(mess)
    mess_data = mess_json['data']
    mess_rep = json.loads(mess_data[i]['replies'])
    mess_rep.append(message)

    mess_data[i]['replies'] = json.dumps(mess_rep)
    mess_json['data'] = mess_data
    mess = mess_json
    ch.messages = json.dumps(mess)
    ch.save()



def send_message(email, channel_id, message):
    channel = Channel.objects.get(id=channel_id)
    mess = channel.messages
    print(type(email))
    mess_json = json.loads(mess)
    mess_info = {'id': get_message_id(channel_id), 'email': email.username, 'message':message, 'replies':json.dumps([])}
    mess_json['data'].append(mess_info)
    print(mess_info)
    channel.messages = json.dumps(mess_json)

    channel.save()
def show_thread(request, channelid, messageid):
    replies = []
    ch = Channel.objects.get(id=channelid)
    repli_data = json.loads(ch.messages)
    print(repli_data['data'])
    for data in repli_data['data']:
        if data['id'] == int(messageid):
            #rep_json = json.loads(data)
            re_rep = data['replies']
            replies.append(re_rep)
    cont = {
        'channel_id':channelid,
        'messid':messageid,
        'replies': replies,
    }
    return render(request, 'thread.html', context=cont)
def show_channel(request, room_name):
    loggedInUser = int(request.session['userid'])
    loggedInEmail = request.session['email']
    print(loggedInUser)
    print(loggedInEmail)
    return render_messages(request, room_name)
    # else:
    #     return HttpResponse("<h1>You are not subscribed to this channel</h1>")
