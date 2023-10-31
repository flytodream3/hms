import uuid, datetime
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
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
    title = models.CharField(
        _('Image title'),
        max_length=255,
        null=True
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

    def __str__(self):
        return self.title


BED_TYPES = (
    ('q', _('Queen')),
    ('k', _('King')),
    ('s', _('Single')),
)


class Room(models.Model):
    uid = models.UUIDField(
        primary_key=True,
        auto_created=True,
        default=uuid.uuid4,
        editable=False
    )
    name = models.CharField(
        _('Name'),
        max_length=70,
        help_text=_('Room number or name')
    )
    images = models.ManyToManyField(
        HotelImage,
        verbose_name=_('Room images'),
        blank=True
    )
    bed_count = models.PositiveSmallIntegerField(
        _('Beds'),
        null=True
    )
    bed_type = models.CharField(
        _('Bed type'),
        max_length=1,
        choices=BED_TYPES,
        null=True
    )
    sleeps = models.PositiveSmallIntegerField(
        _('Sleeps'),
        null=True
    )
    hotel = models.ForeignKey(
        Hotel,
        verbose_name=_('Hotel'),
        on_delete=models.CASCADE
    )
    price = models.DecimalField(
        _('Room price'),
        max_digits=10,
        decimal_places=2,
        default=0,
        null=True, blank=True
    )
    discounted_price = models.DecimalField(
        _('Discounted Price'),
        max_digits=10,
        decimal_places=2,
        null=True, blank=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.SET_NULL,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        _('Updated at'),
        auto_now=True
    )

    class Meta:
        verbose_name = _('Room')
        verbose_name_plural = _('Rooms')

    def __str__(self):
        return f'{self.name} ({self.hotel.name})'


class Reservation(models.Model):
    room = models.ForeignKey(
        Room,
        verbose_name=_('Room'),
        on_delete=models.CASCADE
    )
    number = models.CharField(
        _('Reservation Number'),
        max_length=10,
        blank=True,
        editable=False
    )
    start_date = models.DateField(
        _('Start date')
    )
    end_date = models.DateField(
        _('End date'),
        null=True, blank=True
    )
    duration = models.PositiveIntegerField(
        _('Reservation duration'),
        editable=False,
        null=True, blank=True
    )
    cost = models.DecimalField(
        _('Reservation cost'),
        max_digits=10,
        decimal_places=2,
        null=True, blank=True
    )
    created_at = models.DateTimeField(
        _('Created at'),
        auto_now_add=True
    )
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Author'),
        on_delete=models.CASCADE
    )

    class Meta:
        verbose_name = _('Reservation')
        verbose_name_plural = _('Reservations')

    def __str__(self):
        return self.number

    def save(self, *args, **kwargs):
        if self.end_date <= self.start_date:
            raise ValueError('Start date must be before end date.')
        else:
            total_days = self.end_date - self.start_date
            self.duration = total_days.days
            self.cost = self.duration * self.room.price
            super().save(*args, **kwargs)


@receiver(post_save, sender=Reservation)
def create_reservation_number(sender, instance, created, **kwargs):
    if created and not instance.number:
        instance.number = f'{instance.id:06d}'
        instance.save()