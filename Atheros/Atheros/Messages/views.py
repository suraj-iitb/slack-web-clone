from django.shortcuts import render
from Users.models import User
from Workspaces.models import Channel
from .models import Message
import json
def save_message(user, channel_id, message):
    userobj = User.objects.get(email=user)
    channelobj = Channel.objects.get(id=channel_id)
    mess = Message.objects.create(content=message, replies=json.dumps([]),user=userobj,channels=channelobj)

def save_reply(user, message_id, reply):
    userobj = User.objects.get(email=user)
    messobj = Message.objects.get(id=message_id)
    rep = Replies.objects.create(content=reply, message=messobj, user=userobj)

def delete_message(messageid):
    messid = int(messageid[0:len(messageid)-1])
    print(messid)
    mess = Message.objects.get(id=messid).delete()
