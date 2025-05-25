import uuid
import requests
import os
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import FileResponse

from .models import FileArchive
from .serializers import FileArchiveSerializer


@api_view(['POST'])
@permission_classes([AllowAny]) # IsAuthenticated
def upload_archive(request):
    uploaded_file = request.FILES.get('uploaded_file')
    if not uploaded_file:
        return Response({'error': 'Вы не предоставили файл.'}, status=status.HTTP_400_BAD_REQUEST)

    if not uploaded_file.name.lower().endswith('.zip'):
        return Response({'error': 'Недопустимый тип файла. Допускаются только архивы .zip.'}, status=status.HTTP_400_BAD_REQUEST)

    if request.user.is_authenticated:
        user = request.user
        token = None
    else:
        user = None
        token = uuid.uuid4()

    serializer = FileArchiveSerializer(data=request.data)
    if serializer.is_valid():
        instance = serializer.save(user=user, token=token)
        response_data = serializer.data
        if token:
            response_data['token'] = str(token)
        return Response(response_data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
def process_images(request, archive_id):
    try:
        archive = FileArchive.objects.get(id=archive_id)
    except FileArchive.DoesNotExist:
        return Response({'error': 'Архив не найден.'}, status=status.HTTP_404_NOT_FOUND)

    if not archive.uploaded_file:
        return Response({'error': 'В архив не загружен ни один файл.'}, status=status.HTTP_400_BAD_REQUEST)

    ml_service_url = os.getenv('ML_URL', 'http://ml-service/process/')
    

    try:
        with open(archive.uploaded_file.path, 'rb') as f:
            files = {'file': (archive.uploaded_file.name, f)}
            # Передаем archive_id в данные, чтобы ML сервис знал, какой архив обновлять
            response = requests.post(ml_service_url, files=files, data={'archive_id': archive_id})
            response.raise_for_status()  # Вызываем исключение для плохих статус-кодов
        # ML сервис вызовет endpoint 'receive_processed_archive' после завершения
        return Response({'message': 'Обработка началась. Вы получите уведомление по завершении.'}, status=status.HTTP_202_ACCEPTED)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Не удалось подключиться к ML сервису: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': f'Произошла ошибка: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny])
def receive_processed_archive(request, archive_id):
    try:
        archive = FileArchive.objects.get(id=archive_id)
    except FileArchive.DoesNotExist:
        return Response({'error': 'Архив не найден.'}, status=status.HTTP_404_NOT_FOUND)

    if 'processed_file' not in request.FILES:
        return Response({'error': 'Не предоставлен обработанный файл.'}, status=status.HTTP_400_BAD_REQUEST)

    archive.processed_file = request.FILES['processed_file']
    archive.save()
    serializer = FileArchiveSerializer(archive)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def download_processed_archive(request, archive_id):
    try:
        archive = FileArchive.objects.get(id=archive_id)
    except FileArchive.DoesNotExist:
        return Response({'error': 'Архив не найден.'}, status=status.HTTP_404_NOT_FOUND)

    if not archive.processed_file:
        return Response({'error': 'Файл еще не обработан.'}, status=status.HTTP_404_NOT_FOUND)

    if archive.user:
        if not request.user.is_authenticated or request.user != archive.user:
            return Response({'error': 'Вы не авторизованы.'}, status=status.HTTP_401_UNAUTHORIZED)
    else: # Проверка токена для анонимных пользователей
        token_from_request = request.headers.get('X-Archive-Token')
        if not token_from_request or str(archive.token) != token_from_request:
             # Проверка токена в сессии
            session_token = request.session.get('archive_token')
            if not session_token or str(archive.token) != session_token:
                return Response({'error': 'Недействительный токен или не авторизован.'}, status=status.HTTP_401_UNAUTHORIZED)


    try:
        response = FileResponse(archive.processed_file.open('rb'), as_attachment=True, filename=archive.processed_file.name)
        return response
    except FileNotFoundError:
        return Response({'error': 'Обработанный файл не найден на сервере.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Ошибка при отправке файла: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
