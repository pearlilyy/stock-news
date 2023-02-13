from django.db import models


class Company(models.Model):
    code = models.CharField(max_length=20, primary_key=True)
    company = models.CharField(max_length=40)
    last_update = models.DateField()

    # in Admin page, to see each data title as the company name
    def __str__(self):
        return self.company
