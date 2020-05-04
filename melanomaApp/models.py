from django.db import models

class User(models.Model):
    '''
        the User model
    '''
    username = models.CharField(max_length=20)
    date = models.DateTimeField('registration date')

    def __str__(self):
        return self.username+' '+str(self.date)
