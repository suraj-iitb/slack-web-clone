from django.shortcuts import render
from django.http import HttpResponse
from users.models import users
from users import views
from workspace.models import workspace, Channel
from django.contrib.auth.models import User
import json
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

def invite_workspace(request, workid):
    user = request.session['userid']
    if request.method == 'POST':

        if is_user_admin(workid, user):
            # replace this with send_mail
            views.create_user(request.POST['email'], "password", workid)
            work = {'data':[]}
            user = User.objects.create_user(request.POST.get('email'),request.POST.get('email'),'password')
            print("user: " + str(user))
            user.save()
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
    cont =  {
        'channels': channels,
        'workid': workspace_id,
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
    }
    print(messages)
    return render(request, 'channel.html', context=cont)

def get_message_id(channel_id):
    channel = Channel.objects.get(id=channel_id)
    mess = channel.messages
    mess_json = json.loads(mess)
    if len(mess_json['data']) == 0:
        return 1
    return int(mess_json['data'][len(mess_json['data'])-1]['id']+1)



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

def show_channel(request, room_name):
    loggedInUser = int(request.session['userid'])
    loggedInEmail = request.session['email']
    print(loggedInUser)
    print(loggedInEmail)
    return render_messages(request, room_name)
    # else:
    #     return HttpResponse("<h1>You are not subscribed to this channel</h1>")
