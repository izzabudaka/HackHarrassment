from django.http import HttpResponse

from HackHarrassmentApp.services.DetectionService import DetectionService
from HackHarrassmentApp.services.Model import Model
from HackHarrassmentApp.services.ReaderService import ReaderService

model = Model()
detection_service = DetectionService(model.get_model())
reader = ReaderService()


def index(request):
    return HttpResponse(detection_service.is_harrassment("Fuck You"))
