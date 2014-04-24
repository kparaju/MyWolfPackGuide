# from django.contrib.auth.models import User
# from django.db import models

# class ZipCode(models.Model):
#     pass

# class Address(models.Model):
#     pass  

# class Comment(models.Model):
#     subject = models.CharField(max_length=100)
#     body = models.CharField(max_length=500)
#     user = models.ForeignKey(User)
#     timestamp = models.TimeField(auto_now=True)


# class Event(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.CharField(max_length=500)
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     time = models.DateTimeField(auto_now=False, auto_now_add=False)
#     address = models.ForeignKey(Address)
