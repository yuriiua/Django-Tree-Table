from django.db import models

# Create your models here.

class EmployeeTreeModel(models.Model):
    fullName = models.CharField(max_length=200)
    position = models.CharField(max_length=30)
    salary = models.IntegerField()
    employeeDate = models.DateField()
    bossID = models.IntegerField()
    level = models.IntegerField()
    photo = models.ImageField(upload_to='img',blank=True,null=True)
    bossName = models.CharField(max_length=200)

    def __str__(self):
        return self.fullName