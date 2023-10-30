import uuid, datetime
from django.db import models
from django.conf import settings
from django.utils.translation import gettext_lazy as _


class Hotel(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        _('Hotel name'),
        max_length=300
    )
    stars = models.CharField(
        _('Hotel stars'),
        max_length=1,
        default='1',
        help_text='Hotel stars count from 1 to 5.'
    )
    address = models.CharField(
        _('Hotel Address'),
        max_length=255
    )
    postal_code = models.CharField(
        _('ZIP/Postal code'),
        max_length=15
    )
    city = models.CharField(
        _('City'),
        max_length=70
    )
    state = models.CharField(
        _('State/Province'),
        max_length=70
    )
    country = models.CharField(
        _('Country'),
        max_length=50
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Hotel owner'),
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    deleted = models.BooleanField(
        _('Deleted'),
        default=False
    )
    deleted_at = models.DateTimeField(
        _('Deleted at'),
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Hotel')
        verbose_name_plural = _('Hotels')

    def __str__(self):
        return '%s (%s stars)' % (self.name, self.stars)

    def save(self, *args, **kwargs):
        if self.deleted:
            self.deleted_at = datetime.datetime.now()
        else:
            self.deleted_at = None
        super().save(*args, **kwargs)


class HotelImage(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    file = models.ImageField(
        _('Upload image'),
        upload_to='images/hotels'
    )
    hotel = models.ForeignKey(
        Hotel,
        verbose_name=_('Hotel'),
        on_delete=models.CASCADE
    )
    uploaded = models.DateTimeField(
        _('Date uploaded'),
        auto_now=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        null=True, blank=True
    )

    class Meta:
        verbose_name = _('Image')
        verbose_name_plural = _('Images')
