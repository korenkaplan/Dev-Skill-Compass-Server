from django.db import models
from django.core.validators import MinLengthValidator


class Categories(models.Model):
    name = models.CharField(
        max_length=255, unique=True, validators=[MinLengthValidator(1)]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name.title()}"


class Roles(models.Model):
    name = models.CharField(
        max_length=255, unique=True, validators=[MinLengthValidator(1)]
    )
    description = models.TextField(validators=[MinLengthValidator(1)])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    categories = models.ManyToManyField('Categories')
    # categories = models.ManyToManyField(Categories, through='RoleCategory', related_name='roles')

    def __str__(self):
        return f"{self.name}"


# class RoleCategory(models.Model):
#     role = models.ForeignKey(Roles, on_delete=models.PROTECT)
#     category = models.ForeignKey(Categories, on_delete=models.PROTECT)
#
#     class Meta:
#         unique_together = ('role', 'category')


class Technologies(models.Model):
    name = models.CharField(
        max_length=255, unique=True, validators=[MinLengthValidator(1)]
    )
    category_id = models.ForeignKey(Categories, on_delete=models.PROTECT)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return (
            f"Name: {self.name.title()} | Category: {self.category_id} | ID: {self.id}"
        )


class Synonyms(models.Model):
    origin_tech_id = models.ForeignKey(Technologies, on_delete=models.PROTECT)
    name = models.CharField(
        max_length=255, unique=True, validators=[MinLengthValidator(1)]
    )

    def __str__(self):
        return f"Name: {self.name} | Technology: {self.origin_tech_id.name} | ID: {self.id}"
