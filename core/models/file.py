from django.db import models
from django.contrib.auth.models import User
import hashlib

def generate_file_version_hash(instance, filename):
    # Gera um hash único para cada versão do arquivo
    hash_object = hashlib.sha256()
    hash_object.update(f"{instance.user.id}".encode())
    return f"static/content/{hash_object.hexdigest()[:10]}/{filename}"

class File(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    file_content = models.FileField(upload_to=generate_file_version_hash)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name