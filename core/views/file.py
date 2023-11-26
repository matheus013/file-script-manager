from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.exceptions import APIException
from core.models.file import File
from core.serializers.file import *
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.http import FileResponse

class FileListCreateView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileSerializer

    def post(self, request, *args, **kwargs):
        # Obtém o usuário associado ao token de autenticação
        user = request.user

        # Cria uma cópia mutável dos dados antes de modificá-los
        mutable_data = request.data.copy()
        mutable_data['user'] = user.id

        serializer = FileSerializer(data=mutable_data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise APIException(serializer.errors)
    def get(self, request, *args, **kwargs):
        # Obtém o usuário associado ao token de autenticação
        user = request.user

        # Obtém todos os arquivos associados ao usuário
        files = File.objects.filter(user=user)

        # Serializa os dados dos arquivos
        serializer = FileSerializer(files, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class FileDownloadView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request, file_id, *args, **kwargs):
        try:
            file_obj = File.objects.get(id=file_id, user=request.user)
            response = FileResponse(file_obj.file_content, content_type='application/octet-stream')
            response['Content-Disposition'] = f'attachment; filename="{file_obj.name}"'
            return response
        except File.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=404)