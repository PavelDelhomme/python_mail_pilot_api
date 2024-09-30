from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from .models import Mail, Folder
from .serializers import MailSerializer, FolderSerializer

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_mails(request):
    mails = Mail.objects.filter(user=request.user)
    serializer = MailSerializer(mails, many=True)
    return Response(serializer.data)

@api_view(['POST'])
def send_mail(request):
    serializer = MailSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def manage_folders(request):
    if request.method == 'GET':
        folders = Folder.objects.filter(user=request.user, parent=false)
        serializer = FolderSerializer(folders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)

@api_view(['GET', 'POST'])
def manage_subfolders(request, folder_id):
    parent_folder = Folder.objects.get(id=folder_id)

    if request.method == 'GET':
        subfolders = Folder.objects.filter(parent=parent_folder)
        serializer = FolderSerializer(subfolders, many=True)
        return Response(serializer.data)

    if request.method == 'POST':
        serializer = FolderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user, parent_folder=parent_folder)
            return Response(serializer.data, status=201)
        return Response(serializer.errors, status=400)