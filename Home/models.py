from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import FileExtensionValidator

class User(AbstractUser):
    is_clientUser = models.BooleanField(default=False)
    is_operationUser = models.BooleanField(default=False)

class ClientUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)

class OperationUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)




class Files(models.Model):
    id = models.BigAutoField(primary_key=True)
    File = models.FileField(upload_to='OpsU/', validators=[FileExtensionValidator(['docx','pptx','xlsx', 'pdf'])])

    # def file_name_substring(self):
    #     return str(self.File)[5:] if self.File else ''
    
    # def __str__(self):
    #     return self.id
