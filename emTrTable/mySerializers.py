from rest_framework import serializers
from emTrTable.models import EmployeeTreeModel


class EmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model= EmployeeTreeModel
        fields = ('fullName', 'position', 'photo', 'salary', 'employeeDate', 'bossID', 'level', 'id', 'bossName')
