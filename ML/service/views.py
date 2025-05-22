from django.http import JsonResponse
from django.views import View
from django.conf import settings
from .engine import main as engine_run
import os

class ProcessImagesView(View):
    def get(self, request):
        try:
            engine_run()
            return JsonResponse({'status': 'success', 'message': 'Images processed successfully.'})
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=500)