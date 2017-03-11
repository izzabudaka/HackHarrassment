from django.http import HttpResponse
import json

from HackHarrassmentApp.services.DetectionService import DetectionService
from HackHarrassmentApp.services.Model import Model
from HackHarrassmentApp.services.ReaderService import ReaderService
from HackHarrassmentApp.services.ChatService import ChatService

model = Model()
detection_service = DetectionService(model.get_model())
reader = ReaderService()
chat_service = ChatService()

def index(request):
    return HttpResponse(detection_service.is_harrassment("Fuck You"))

def create_user(request):
    return HttpResponse(chat_service.add_user("Alex"))


def get_relations(request):
    relations = chat_service.get_all_relations()
    return HttpResponse(json.dumps(relations))


def get_users(request):
    after = request.GET.get('user_id', 0)
    users = chat_service.get_all_users_after(after)
    user_data = []
    for user in users:
        user_data.append({
            'id': user[0],
            'name': user[1],
            'tagged': user[2]
        })
    return HttpResponse(json.dumps(user_data))


def get_latest_messages(request):
    row_id = request.GET.get('last_msg', 4294967295)
    result = chat_service.get_messages_after(row_id)
    messages = []
    for message in result:
        messages.append({
            'id': message[0],
            'sender': message[1],
            'receiver': message[2],
            'msg': message[3]
        })
    return HttpResponse(json.dumps(messages))
