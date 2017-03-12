from django.http import HttpResponse
import json

from sklearn.feature_extraction.text import TfidfVectorizer

from HackHarrassmentApp.services.DetectionService import DetectionService
from HackHarrassmentApp.services.Model import Model
from HackHarrassmentApp.services.ReaderService import ReaderService
from HackHarrassmentApp.services.ChatService import ChatService

tfidf_vect = TfidfVectorizer()
model = Model(tfidf_vect)
model.clean()
detection_service = DetectionService(model.get_model(), model.get_svm(), tfidf_vect)
reader = ReaderService()
chat_service = ChatService()


def index(request):
    return HttpResponse(detection_service.is_harrassment(request.POST.get("txt")))


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
    row_id = request.GET.get('last_msg')
    if row_id is None:
        return HttpResponse(chat_service.get_last_message_id())
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


def post_message(request):
    sender = request.POST.get('sender')
    message = request.POST.get('message')

    if sender is None:
        return HttpResponse('Sender not defined')
    if message is None:
        return HttpResponse('Message not defined')

    if chat_service.user_exists(sender) is None:
        return HttpResponse('That user does not exist')

    str_data = unicode.split(message)

    if len(str_data) < 2:
        return HttpResponse("Invalid message")

    receiver = str_data[0]
    message = ' '.join(str_data[1:])

    if receiver[:1] != '@':
        return HttpResponse("Invalid receiver")
    receiver = receiver[1:]

    if chat_service.user_exists(receiver) is None:
        return HttpResponse('Receiver does not exist')

    return HttpResponse(chat_service.insert_message(sender, receiver, message))



