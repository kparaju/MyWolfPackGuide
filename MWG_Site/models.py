from django.contrib.auth.models import User
from django.db import models
from django.core.files.storage import FileSystemStorage
from django.utils.translation import gettext as _
from MyWolfpackGuide import settings
from django.db.models.signals import post_save
from django.core.urlresolvers import reverse

fs = FileSystemStorage(location=settings.MEDIA_ROOT)

class MWGUser(models.Model):
    user       = models.OneToOneField(User)
    picture    = models.ImageField(_(u'picture'), upload_to='users', db_column='picture', blank=True, null=True)

    class Meta:
        verbose_name        = 'MyWolfpackGuide User'
        verbose_name_plural = 'MyWolfpackGuide Users'

    def __unicode__(self):
        return unicode(self.name)

    @property
    def name(self):
        return "{} {}".format(self.user.first_name, self.user.last_name)

    @property
    def events(self):
        return Event.objects.filter(created_by=self.user)

    @property
    def is_admin(self):
        return MWGAdmin.objects.filter(user=self.user).exists()


    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            MWGUser.objects.create(user=instance)
            # new_user.picture = instance.social_auth.get(provider='google-oauth2').extra_data['picture'] 

    post_save.connect(create_user_profile, sender=User)


class MWGAdmin(MWGUser):

    class Meta:
        verbose_name = 'MyWolfpackGuide Admin'
        verbose_name_plural = 'MyWolfpackGuide Admins'

    def __unicode__(self):
        return unicode(self.name)



class Address(models.Model):
    line_1       = models.CharField(max_length=100, null=True)
    line_2       = models.CharField(max_length=100, null=True, blank=True)
    city         = models.CharField(max_length=100, null=True)
    state_abbrev = models.CharField(max_length=2, null=True)
    zipcode      = models.CharField(max_length=5, null=True, blank=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

    @property
    def get_address(self):
        return "{} {}, {} {}, {}".format(self.line_1, self.line_2, self.city, self.zipcode, self.state_abbrev)

    def __unicode__(self):
        return unicode("{} {}, {}, {}".format(self.line_1, self.line_2, self.city, self.state_abbrev))


class Event(models.Model):
    name        = models.CharField(max_length=100, null=True)
    picture     = models.ImageField(_(u'picture'), upload_to='events', db_column='picture', blank=True, null=True)
    description = models.CharField(max_length=500, null=True)
    price       = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    time        = models.DateTimeField(auto_now=False, auto_now_add=False, null=True)
    address     = models.ForeignKey(Address)
    created_by  = models.ForeignKey(MWGUser)

    def __unicode__(self):
        return unicode(self.name)

    def get_absolute_url(self):
        return reverse('event-details', kwargs={'pk': self.pk})



