from django.shortcuts import render
from django.http import HttpResponse
from users.models import users
from users import views
from workspace.models import workspace, Channel
import json
# Create your views here.

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

        users = "[{user_id: %s, email: %s, isAdmin:True},]"%(userid, username)
        channels = {'data':[]}
        users_json = json.dumps(users)
        channels_json = json.dumps(channels)

        work = workspace(workspace_name=name, users=users_json, channels=channels_json)
        work.save()

        views.append_workspace(userid, work.id, work.workspace_name, work.channels)

        return views.send_data(request)

    else:
        return render(request, 'create.html', {})

def show_workspace(request, workspace_id):
    workspaces = workspace.objects.get(id=int(workspace_id))
    workspace_channel = workspaces.channels
    workspace_channel_json = json.loads(workspace_channel)
    print(type(workspace_channel_json))
    channels = []
    for data in workspace_channel_json['data']:
        channels.append([data['name'], data['id']])

    cont =  {
        'channels': channels,
        'workid': workspace_id,
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
