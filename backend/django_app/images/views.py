import uuid
import requests
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.http import FileResponse
from .models import FileArchive
from .serializers import FileArchiveSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_archive(request):
    if request.user.is_authenticated:
        user = request.user
        token = None
    else:
        user = None
        token = uuid.uuid4()

    serializer = FileArchiveSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save(user=user, token=token)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@permission_classes([AllowAny]) # Or IsAuthenticated if only authenticated users can trigger processing
def process_images(request, archive_id):
    try:
        archive = FileArchive.objects.get(id=archive_id)
    except FileArchive.DoesNotExist:
        return Response({'error': 'Archive not found'}, status=status.HTTP_404_NOT_FOUND)

    if not archive.uploaded_file:
        return Response({'error': 'No file uploaded to this archive'}, status=status.HTTP_400_BAD_REQUEST)

    # Construct the full URL for the ML service
    # Assuming the ML service expects the file data in the request body
    ml_service_url = "http://ml-service/process/"
    try:
        with open(archive.uploaded_file.path, 'rb') as f:
            files = {'file': (archive.uploaded_file.name, f)}
            # Include archive_id in the data payload so ML service knows which archive to update
            response = requests.post(ml_service_url, files=files, data={'archive_id': archive_id})
            response.raise_for_status()  # Raise an exception for bad status codes
        # Assuming ML service will call 'receive_processed_archive' endpoint upon completion
        return Response({'message': 'Processing started. You will be notified upon completion.'}, status=status.HTTP_202_ACCEPTED)
    except requests.exceptions.RequestException as e:
        return Response({'error': f'Failed to connect to ML service: {str(e)}'}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    except Exception as e:
        return Response({'error': f'An error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(['POST'])
@permission_classes([AllowAny]) # Or specific permissions based on your ML service's auth
def receive_processed_archive(request, archive_id):
    try:
        archive = FileArchive.objects.get(id=archive_id)
    except FileArchive.DoesNotExist:
        return Response({'error': 'Archive not found'}, status=status.HTTP_404_NOT_FOUND)

    if 'processed_file' not in request.FILES:
        return Response({'error': 'No processed file provided'}, status=status.HTTP_400_BAD_REQUEST)

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
        return Response({'error': 'Archive not found'}, status=status.HTTP_404_NOT_FOUND)

    if not archive.processed_file:
        return Response({'error': 'File has not been processed yet.'}, status=status.HTTP_404_NOT_FOUND)

    if archive.user:
        if not request.user.is_authenticated or request.user != archive.user:
            return Response({'error': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)
    else: # Anonymous user, check token
        # Assuming token is passed in headers or as a query parameter for simplicity
        # For session-based token, you'd retrieve it from request.session
        token_from_request = request.headers.get('X-Archive-Token') # Example: token in header
        if not token_from_request or str(archive.token) != token_from_request:
             # Fallback: check if token is in session (if you implement session storage for anonymous users)
            session_token = request.session.get('archive_token')
            if not session_token or str(archive.token) != session_token:
                return Response({'error': 'Invalid token or unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)


    try:
        response = FileResponse(archive.processed_file.open('rb'), as_attachment=True, filename=archive.processed_file.name)
        return response
    except FileNotFoundError:
        return Response({'error': 'Processed file not found on server.'}, status=status.HTTP_404_NOT_FOUND)
    except Exception as e:
        return Response({'error': f'Error serving file: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 