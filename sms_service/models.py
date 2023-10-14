from django.db import models

class Mutualist(models.Model):
    full_name = models.CharField("Nom Prénom", max_length=100)
    phone = models.CharField("Numéro de télephone", max_length=10)

    def __str__(self):
        return self.full_name
    
    class Meta:
        verbose_name = "Mutualiste"
        verbose_name_plural = "Mutualistes"



class Sms(models.Model):

    content = models.TextField("contenu")
    mutualists = models.ManyToManyField(Mutualist)



    class Meta:
        verbose_name = "sms à envoyer"
        verbose_name_plural = "sms à envoyer"
        

    def __str__(self):
        return "Sms à envoyer"