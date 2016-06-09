from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.validators import RegexValidator

from . import managers

# Create your models here.
class Profile(models.Model):
    # Relations
    user = models.OneToOneField(
           settings.AUTH_USER_MODEL,
           related_name='profile',
           verbose_name=_('user')
           )

    # Attributes - Mandatory
    interaction = models.PositiveIntegerField(
                  default=0,
                  verbose_name=_('interaction')
                  )

    # Attributes - Optional

    # Object Manager
    objects = managers.ProfileManager()

    # Custom properties
    @property
    def username(self):
        return self.user.username

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _('Profile')
        verbose_name_plural = _('profiles')
        ordering = ('user',)

    def __str__(self):
        return self.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_profile_for_new_user(sender, created, instance, **kwargs):
    if created:
        profile = Profile(user=instance)
        profile.save()


class Project(models.Model):

    # Relations
    user = models.ForeignKey(
           Profile,
           related_name='projects',
           verbose_name=_('name')
           )

    # Attributes - Mandatory
    name = models.CharField(
           max_length=100,
           verbose_name=_('name'),
           help_text=_('Enter the project name')
           )
    color = models.CharField(
           max_length=7,
           default='#fff',
           validators=[RegexValidator('(^#[0-9a-fA-F]{3}$)|(^#[0-9a-fA-F]{6}$)')],
           verbose_name=_('color'),
           help_text=_('Enter the hex color code, like #ccc or #cccccc')
           )

    # Attributes - Optional
    # Object Manager
    objects = managers.ProjectManager()

    # Custom properties

    # Methods

    # Meta and String
    class Meta:
        verbose_name = _('Project')
        verbose_name_plural = _('Projects')
        ordering = ('user', 'name')
        unique_together = ('user', 'name')

    def __str__(self):
        return '{user} - {name}'.format(user=self.user, name=self.name)


class Tag(models.Model):
    # Relations
    user = models.ForeignKey(
              Profile,
              related_name='tags',
              verbose_name=_('user'))
    # Attributes - Mandatory
    name = models.CharField(
    max_length=100,
    verbose_name=_('Name')
    )

    # Attributes - Optional
    # Object Manager
    objects = managers.TagManager()
    # Custom properties
    # Methods

    # Meta and String
    class Meta:
        verbose_name = _('Tag')
        verbose_name_plural = _('Tags')
        ordering = ('user', 'name',)
        unique_together = ('user', 'name',)

    def __str__(self):
        return '{} - {}'.format(self.user, self.name)
