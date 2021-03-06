from django.db import models
from django.contrib.auth.models import PermissionsMixin
from django.contrib.auth.base_user import AbstractBaseUser
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.base_user import BaseUserManager

# Create your models here.
from auth_.base_models import DeckMixin, CardMixin, ContentMixin
from core.models import DeckTemplate, CardTemplate
from utils.constants import STATES, STATE_DEFAULT


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    is_active = models.BooleanField(_('active'), default=True)
    is_staff = models.BooleanField(_('is_staff'), default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')


class Profile(models.Model):
    phone_number = models.CharField(max_length=30, blank=True)
    location = models.CharField(max_length=30, blank=True)
    user = models.OneToOneField(CustomUser, related_name="profile", on_delete=models.CASCADE)

    class Meta:
        verbose_name = '??????????????'
        verbose_name_plural = '??????????????'


class Deck(DeckMixin):
    progress = models.IntegerField(default=0)
    template = models.ForeignKey(DeckTemplate, on_delete=models.CASCADE)
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)


class Card(CardMixin):
    status = models.SmallIntegerField(choices=STATES, default=STATE_DEFAULT)
    template = models.ForeignKey(CardTemplate, on_delete=models.CASCADE)
    deck = models.ForeignKey(Deck, on_delete=models.CASCADE, related_name="deck_cards")


class ContentFragment(ContentMixin):
    upload = models.ForeignKey(CardTemplate, related_name="contents", on_delete=models.CASCADE)


class ContentFragmentForCard(ContentMixin):
    upload = models.ForeignKey(Card, related_name="contents", on_delete=models.CASCADE)
