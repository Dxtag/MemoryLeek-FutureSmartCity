from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _


class Car(models.Model):
    owner = models.ForeignKey(get_user_model(), verbose_name=("Owner"), related_name="cars", on_delete=models.CASCADE)
    name = models.CharField(_("Name"), max_length=128)

    def __str__(self):
        return self.name
    def __repr__(self):
        return self.__str__()
    
