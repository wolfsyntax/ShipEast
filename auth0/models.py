from django.db import models
from django.conf import settings
from django.contrib.auth.models import User


PARISH = (
    ('', 'Choose...'),
    ('St. Andrew', 'Kingston'),
    ('Portland', 'St. Thomas'),
    ('St. Catherine', 'St. Mary'),
    ('St. Ann', 'Manchester',),
    ('Clarendon', 'Hanover',),
    ('Westmoreland', 'St. James',),
    ('Trelawny', 'St. Elizabeth')
)

class Profile(models.Model):

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date_of_birth = models.DateField(blank=True, null=True)
    photo = models.ImageField(upload_to='users/%Y/%m/%d', blank=True)

    def __str__(self):
        return 'Profile for user {}'.format(self.user)

    class Meta:
    	db_table='Profile'

class Detail(models.Model):
	
	user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	phone = models.CharField(max_length=10)
	trn = models.CharField(max_length=9)
	address = models.CharField(max_length=254)
	parish = models.CharField(choices=PARISH, max_length=15)
	
	def __str__(self):
		return "TRN for user {}".format(self.trn)

	class Meta:
		db_table = 'Detail'

class Document(models.Model):

    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
    	db_table = 'Document'