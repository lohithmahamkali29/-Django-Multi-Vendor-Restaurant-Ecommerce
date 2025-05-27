from django.db.models.signals import post_save,pre_save
from django.dispatch import receiver
from .models import User,userProfile







@receiver(post_save, sender=User )
def post_save_create_profile_receiver(sender, instance, created, **kwargs):
   print(created)
   if created:
        userProfile.objects.create(user=instance)
        print('user profile is created')
   else:
        try:
           profile = userProfile.objects.create(user=instance)
           profile.save()
        except userProfile.DoesNotExist :
            userProfile.objects.create(user=instance)
            print('profile was not exist,but i created one')
        print('user is updated')
# post_save.connect(post_save_create_profile_receiver, sender=User)
@receiver(pre_save, sender=User)
def pre_save_profile_receiver(sender, instance, **kwargs):
    print(instance.username,'this user is being saved') 


