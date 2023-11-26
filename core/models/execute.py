from django.db import models
from django.contrib.auth.models import User

class FileScript(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    script_name = models.CharField(max_length=255)
    script_content = models.TextField()
    applied_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.script_name}"
