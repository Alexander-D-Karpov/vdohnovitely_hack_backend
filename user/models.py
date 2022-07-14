from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class User(AbstractUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=20, unique=True)
    subscriber_count = models.PositiveIntegerField(default=0)
    telephone = PhoneNumberField(blank=True)

    # characteristics
    communication = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    idea_generation = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    organisation = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    creativity = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    resource_search = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    achievement = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    critical_thinking = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )
    leadership = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(6)], blank=True, null=True
    )

    # why section
    want_to_find_out = models.TextField(blank=True)
    want_to_learn = models.TextField(blank=True)
    want_to_get = models.TextField(blank=True)

    # who am I
    introvert = models.BooleanField(default=False, blank=True)
    individualist = models.BooleanField(default=False, blank=True)
    optimist = models.BooleanField(default=False, blank=True)
    serious = models.BooleanField(default=False, blank=True)
    organized = models.BooleanField(default=False, blank=True)
    leader = models.BooleanField(default=False, blank=True)

    who_am_i_extra_1 = models.CharField(max_length=50, blank=True)
    who_am_i_extra_2 = models.CharField(max_length=50, blank=True)
    who_am_i_extra_3 = models.CharField(max_length=50, blank=True)
    who_am_i_extra_4 = models.CharField(max_length=50, blank=True)
    who_am_i_extra_5 = models.CharField(max_length=50, blank=True)

    # what I want
    what_i_want_1 = models.CharField(max_length=100, blank=True)
    what_i_want_2 = models.CharField(max_length=100, blank=True)
    what_i_want_3 = models.CharField(max_length=100, blank=True)
    what_i_want_4 = models.CharField(max_length=100, blank=True)
    what_i_want_5 = models.CharField(max_length=100, blank=True)
    what_i_want_6 = models.CharField(max_length=100, blank=True)
    what_i_want_7 = models.CharField(max_length=100, blank=True)
    what_i_want_8 = models.CharField(max_length=100, blank=True)
    what_i_want_9 = models.CharField(max_length=100, blank=True)
    what_i_want_10 = models.CharField(max_length=100, blank=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def images(self):
        return [x.image for x in DreamAssociation.objects.filter(user=self)]


class DreamAssociation(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="dream_images"
    )
    image = models.ImageField(upload_to="uploads/", blank=False)


class Subscriber(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscribers"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="subscriptions"
    )

    class Meta:
        unique_together = ("author", "user")
