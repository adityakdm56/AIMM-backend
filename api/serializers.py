from rest_framework import serializers
from .models import *


class DepartmentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Department
        fields = ('name', 'id')


class UserSerializer(serializers.ModelSerializer):
    dept = serializers.CharField(
        source='department.name', read_only=True)

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'designation', 'team', 'dept')


class DepartmentWithUsersSerializer(serializers.ModelSerializer):
    user = UserSerializer(
        source="user_set", many=True)

    class Meta:
        model = Department
        fields = ('name', 'id', 'user')


# ADITYA

class TeamSerializer(serializers.ModelSerializer):
    members = UserSerializer(source="user_set", many=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'head', 'members')


class EquipmentSerializer(serializers.ModelSerializer):
    dept = serializers.CharField(source="department.name", read_only=True)
    teams = TeamSerializer( many=True)
    class Meta:
        model = Equipment
        fields = ("serial_no", "name", "description", "priority",
                  "location", "installation_date", "maintenance_latency", "dept", "teams")


class EquipmentModificationSerializer(serializers.ModelSerializer):

    class Meta:
        model = Equipment
        fields = ('name', 'description', 'priority',
                  'location', 'maintenance_latency')


class MaintenanceTicketSerializer(serializers.ModelSerializer):
    equipment = serializers.CharField(source='equipment.name', read_only=True)
    raised_by = serializers.CharField(
        source='raised_by.name', read_only=True)

    class Meta:
        model = MaintenanceTicket
        fields = ('id', 'description', 'raised_by', 'issue_date', 'status', 'equipment',
                  'resolution_date', 'technician_assigned', 'teams', 'technician_completed')


class UserRequestSerializer(serializers.ModelSerializer):
    department = serializers.CharField(
        source='department.name', read_only=True)
    teams = TeamSerializer( many=True)
    class Meta:
        model = UserRequest
        fields = ('id', 'name', 'email', 'department', 'designation', 'status')




# ADITYA


class EquipmentMaintenanceSerializer(serializers.ModelSerializer):

    maintenanceTicket = MaintenanceTicketSerializer(
        source='maintenanceticket_set', many=True)

    class Meta:
        model = Equipment
        fields = ('serial_no', 'maintenanceTicket')


# ******************************************AJAY************************
#
class EquipmentSerializerAJ(serializers.ModelSerializer):
    class Meta:
        model = Equipment
        fields = ('serial_no', 'name', 'department', 'description',
                  'priority', 'location', 'installation_date', 'maintenance_latency', 'teams')

        extra_kwargs = {'installation_date': {'required': False}}


# class MaintenanceTicketSerializerAJ(serializers.ModelSerializer):
#     # equipment = EquipmentSerializer(
#     #     source="equipment.serial_no")

#     class Meta:
#         model: MaintenanceTicket

#         fields = ('equipment', 'description', 'issue_date',
#                   'resolution_date', 'raised_by', 'technician_assigned')

#         extra_kwargs = {'issue_date': {'required': False},
#                         'resolution_date': {'required': False},
#                         'technician_assigned': {'required': False}}


# class UserRequestSerializerAJ(serializers.ModelSerializer):
#     department = DepartmentSerializer(read_only=True)

#     class Meta:
#         model: UserRequest
#         fields = ('name', 'email', 'department',
#                   'designation', 'date_raised', 'status')

#         extra_kwargs = {'date_raised': {'required': False},
#                         'status': {'required': False}}
