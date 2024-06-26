from data_importers.event_types import DataEventType
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django_extensions.db.models import TimeStampedModel
from file_uploads.models import Upload


class DataEvent(TimeStampedModel):
    council = models.ForeignKey("councils.Council", on_delete=models.CASCADE)
    upload = models.ForeignKey(Upload, null=True, on_delete=models.CASCADE)
    event_type = models.CharField(choices=DataEventType.choices)
    election_dates = ArrayField(models.DateField(), default=list)
    metadata = models.JSONField(default=dict)
    payload = models.JSONField(default=dict)


class DataQuality(models.Model):
    class Meta:
        verbose_name_plural = "Data Quality"

    def __unicode__(self):
        return "Data quality for %s" % self.council

    council = models.OneToOneField(
        "councils.Council",
        primary_key=True,
        on_delete=models.CASCADE,
    )
    report = models.TextField(blank=True)
    num_stations = models.IntegerField(default=0)
    num_districts = models.IntegerField(default=0)
    num_addresses = models.IntegerField(default=0)
