from django.db import models


class Author(models.Model):
    name = models.CharField(max_length=200, null=False)
    born_date = models.DateField(blank=True, null=True)
    born_location = models.CharField(max_length=200, blank=True, null=True)
    descryption = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.name}"

    
class Tag(models.Model):
    name = models.CharField(max_length=200, null=False, unique=True)

    def __str__(self):
        return f"{self.name}"
    

class Quote(models.Model):
    quote = models.TextField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return f"{self.quote}"