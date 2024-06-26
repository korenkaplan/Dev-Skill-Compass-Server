from django.db import models
from core.models import Technologies, Roles
from django.core.validators import MinValueValidator


class MonthlyTechnologiesCounts(models.Model):
    role_id = models.ForeignKey(Roles, on_delete=models.PROTECT)
    technology_id = models.ForeignKey(Technologies, on_delete=models.PROTECT)
    counter = models.IntegerField(default=0, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        date_formatted = self.updated_at.strftime("%d/%m/%Y")
        created_date_formatted = self.created_at.strftime("%d/%m/%Y")
        return (
            f"ID: {self.id} | Tech: {self.technology_id.name.title()} | Amount: {self.counter} |"
            f" Role: {self.role_id}| Created At: {created_date_formatted}  | Updated To: {date_formatted} "
        )

    class Meta:
        indexes = [
            models.Index(fields=['role_id', 'technology_id'])
        ]


class HistoricalTechCounts(models.Model):
    technology_id = models.ForeignKey(Technologies, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Roles, on_delete=models.PROTECT)
    counter = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date_formatted = self.created_at.strftime("%d/%m/%Y")
        return (
            f"ID: {self.id} | Tech: {self.technology_id.name.title()} |"
            f" Amount: {self.counter} | Role: {self.role_id} | Created At: {date_formatted} "
        )

    class Meta:
        indexes = [
            models.Index(fields=['role_id', 'technology_id']),
            models.Index(fields=['created_at'])
        ]


class AggregatedTechCounts(models.Model):
    technology_id = models.ForeignKey(Technologies, on_delete=models.PROTECT)
    role_id = models.ForeignKey(Roles, on_delete=models.PROTECT)
    counter = models.IntegerField(default=1, validators=[MinValueValidator(0)])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        date_formatted = self.created_at.strftime("%d/%m/%Y")
        return (
            f"ID: {self.id} | Tech: {self.technology_id.name.title()} |"
            f" Amount: {self.counter} | Role: {self.role_id} | Created At: {date_formatted} "
        )

    class Meta:
        indexes = [
            models.Index(fields=['role_id', 'technology_id']),
        ]
