from django.db import models
from uuid import uuid4
from django.utils import timezone


class TimeStampedBaseModel(models.Model):
    """Base model with timestamp information that is common to many models. """

    class Meta:
        abstract = True

    created_at = models.DateTimeField(
        default=None,
        blank=True,
        null=True,
        help_text="DateTime this model instance was created.")
    updated_at = models.DateTimeField(
        default=timezone.now,
        help_text="DateTime this model instance was last updated.")

    def save(self, *args, **kwargs):
        current_time = timezone.now()
        if self.uuid is None:
            self.created_at = current_time
        self.updated_at = current_time
        return super(TimeStampedBaseModel, self).save(*args, **kwargs)


class School(TimeStampedBaseModel):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False, )
    name = models.CharField(
        max_length=255,
        unique=True,
        default="Example",
        blank=True,
        null=True,
        help_text="Name of school.")
    address = models.TextField(
        default=None,
        blank=True,
        null=True,
        help_text="Address of the school.")

    def __unicode__(self):
        return self.uuid


class Classroom(TimeStampedBaseModel):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False, )
    name = models.CharField(
        max_length=255,
        unique=False,
        default="1A",
        blank=False,
        null=False,
        help_text="Name of classroom.")
    school = models.ForeignKey(
        School,
        related_name='classrooms')

    class Meta:
        unique_together = (('school', 'name'),)

    def __unicode__(self):
        return self.uuid


class Student(TimeStampedBaseModel):
    uuid = models.UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False, )
    firstname = models.CharField(
        verbose_name="First Name",
        max_length=30,
        default="",
        blank=False,
        null=False,
        help_text="The student's first name")
    middlenames = models.CharField(
        verbose_name="Middle Names",
        max_length=30,
        default=None,
        blank=True,
        null=True,
        help_text="The student's middle names (space separated, if multiple)")
    lastname = models.CharField(
        verbose_name="Last Name",
        max_length=30,
        default="",
        blank=False,
        null=False,
        help_text="The student's last name", )
    is_active = models.BooleanField(
        default=True,
        help_text="True if student has not graduated, left, or been expelled")
    is_suspended = models.BooleanField(
        default=False,
        help_text="True if student is currently on suspension")
    classroom = models.ForeignKey(
        Classroom,
        related_name='students')

    def __unicode__(self):
        return self.uuid
