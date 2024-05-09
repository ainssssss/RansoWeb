from django.db import models

class File(models.Model):
    FileName = models.CharField(max_length=9999999999999)
    Content = models.TextField(max_length=9999999999999)
    UploadedDate = models.DateTimeField(auto_now_add=True,blank=True)
    
    def __str__(self):
        return str(self.FileName)


class UserRansom(models.Model):
    UserName = models.CharField(max_length=9999999999999)
    Published = models.BooleanField(default=False) # E: Argument of type "Literal[False]" cannot be assigned to parameter "default" of type "type[NOT_PROVIDED]" in function…
    Files = models.ManyToManyField(File)
    CertsLocation = models.CharField(max_length=200)
    CreationDate = models.DateTimeField(auto_now_add=True)
    CertsPassword = models.CharField(max_length=8)

    def __str__(self): # E: Method "__str__" overrides class "Model" in an incompatible manner   Return type mismatch: base method returns type "str", override returns type…
          return self.UserName

