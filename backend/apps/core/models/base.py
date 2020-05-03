from django.db import models
from django.conf import settings

class Author(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                                on_delete=models.CASCADE,
                                null=True)

    class Meta:
      abstract = True

    def __str__(self):
        return self.author
