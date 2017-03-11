from django.http import HttpResponse

from HackHarrassmentApp.services.DetectionService import DetectionService

detection_service = DetectionService()


def index(request):
    return HttpResponse(detection_service.get_next())
