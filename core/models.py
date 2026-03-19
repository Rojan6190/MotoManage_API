from django.db import models
import uuid

class BaseModel(models.Model):
    pass

    class Meta:
        abstract = True