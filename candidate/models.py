from django.db import models


GENDER_CHOICES = [('male', 'MALE'),
                  ('female', 'FEMALE'),
                  ('other', 'OTHER') 
                ]

class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True

class Candidate(TimeStampModel):
    name = models.CharField(max_length=100, null=False, blank=False)
    age = models.IntegerField()
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    email = models.EmailField(null=False, blank=False, unique=True)
    phone = models.CharField(max_length=15, null=False, blank=False)

    def __str__(self):
        return f"{self.name} ({self.email})" 
