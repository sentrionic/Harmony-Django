from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.conf import settings
from rest_framework.authtoken.models import Token
from django.core import validators


class MyAccountManager(BaseUserManager):

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        if not username:
            raise ValueError('Users must have a username')

        user = self.model(
            email=self.normalize_email(email),
            username=username
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


def upload_location(instance, filename):
    file_path = 'account/{author_id}/{filename}'.format(
        author_id=str(instance.id), filename=filename)
    return file_path


class Account(AbstractBaseUser):
    email = models.EmailField(verbose_name="email", max_length=60, unique=True)
    username = models.CharField(max_length=30, unique=True, validators=[
                                validators.RegexValidator(
                                r'^[\w.@+-]+$', 'Enter a valid username. Letters, digits and '
                                '@/./+/-/_ only.', 'invalid')])
    image = models.ImageField(upload_to=upload_location, default='default.png', null=False, blank=True)
    display_name = models.CharField(verbose_name="display name", default="", max_length=30, blank=True)
    description = models.CharField(verbose_name="description", default="", max_length=100, blank=True)
    website = models.CharField(verbose_name="website", default="", max_length=30, blank=True)
    posts = models.IntegerField(verbose_name="posts", default=0)
    followers = models.IntegerField(verbose_name="followers", default=0)
    following = models.IntegerField(verbose_name="following", default=0)
    date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = MyAccountManager()

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        if self.display_name is None:
            self.display_name = self.username
        super().save(*args, **kwargs)

    # For checking permissions. to keep it simple all admin have ALL permissons
    def has_perm(self, perm, obj=None):
        return self.is_admin

    # Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
    def has_module_perms(self, app_label):
        return True


@receiver(post_delete, sender=Account)
def submission_delete(sender, instance, **kwargs):
    instance.image.delete(False)


class Follows(models.Model):
    follower = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='follower')
    following = models.ForeignKey(Account, on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Follow"
        verbose_name_plural = "Follows"


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
