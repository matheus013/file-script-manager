from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from core.models.execute import FileScript
from core.serializers.execute import FileScriptSerializer
import subprocess


def create_file(file_path, content):
    try:
        with open(file_path, 'w') as file:
            file.write(content)
        print(f'Arquivo criado com sucesso: {file_path}')
    except Exception as e:
        print(f'Erro ao criar o arquivo: {e}')
        
def delete_file(file_path):
    try:
        os.remove(file_path)
        print(f'Arquivo apagado com sucesso: {file_path}')
    except Exception as e:
        print(f'Erro ao apagar o arquivo: {e}')

class ApplyScriptToFileDialogView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    
    def post(self, file_id, script_id, request, *args, **kwargs):
        try:
            # Obtém o usuário associado ao token de autenticação
            user = request.user

            # Obtém o arquivo e o script associados aos IDs fornecidos
            file_obj = File.objects.get(id=file_id, user=user)
            script_obj = FileScript.objects.get(id=script_id, user=user)
            
            create_file(script_obj.script_name, script_obj.script_content)

            

            # Comando Bash a ser executado
            bash_command = f"python {script_obj.script_name} {file_obj.file_content.name}"

            try:
                # Executa o comando Bash
                result = subprocess.run(bash_command, shell=True, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

                # Imprime a saída do comando
                print("Saída do Comando:")
                script_result = result.stdout

            except subprocess.CalledProcessError as e:
                # Se ocorrer um erro, imprime a mensagem de erro
                print("Erro ao executar o comando Bash:")
                print(e.stderr)
                
            response_data = {
                'script_id': script_id,
                'file_id': file_id,
                'script_result': script_result,
            }
            
            delete_file(script_obj.script_name)
            
            return Response(response_data, status=status.HTTP_200_OK)

        except File.DoesNotExist:
            return Response({'detail': 'File not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        



class FileScriptListCreateView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = FileScriptSerializer

    def get_queryset(self):
        # Retorna todos os scripts associados ao usuário atual
        return FileScript.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        # Associa o usuário atual ao script antes de salvá-lo
        serializer.save(user=self.request.user)

class FileScriptDetailView(RetrieveUpdateDestroyAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = FileScript.objects.all()
    serializer_class = FileScriptSerializer
