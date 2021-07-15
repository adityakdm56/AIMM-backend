from django.db import models



class Department(models.Model):
    name = models.CharField(max_length=50, unique=False,
                            default="", editable=True)
    #head = models.OneToOneField(User, on_delete=models.CASCADE, null=True)
    head = models.IntegerField(unique=True)

    def __str__(self):
        return self.name+" - "


class Team(models.Model):
    name = models.CharField(max_length=50, unique=False,
                            default="", editable=True)
    head = models.IntegerField(unique=True)


class User(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, default="", editable=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    id = models.IntegerField(unique=True, primary_key=True)
    department = models.ForeignKey(
        Department,  on_delete=models.CASCADE, null=True)
    designation = models.CharField(
        max_length=5, unique=False, default="", editable=True)
    date_added = models.DateField(auto_now_add=True)
    # user will have team if it is of maintainance dept(sub dept of maintenance dept)
    team = models.ForeignKey(
        Team, on_delete=models.DO_NOTHING, null=True, blank=True)


class Equipment(models.Model):
    serial_no = models.CharField(
        max_length=50, primary_key=True, default="", editable=True)
    name = models.CharField(max_length=50, unique=False,
                            default="", editable=True)
    department = models.ForeignKey(
        Department, on_delete=models.CASCADE, default="1")
    description = models.CharField(
        max_length=100, unique=False, default="", editable=True)
    priority = models.PositiveIntegerField()
    location = models.CharField(max_length=100, unique=False,
                                default="", editable=True)
    installation_date = models.DateField(auto_now_add=True)
    maintenance_latency = models.PositiveIntegerField(default=30)
    teams = models.ManyToManyField(Team, related_name="default_teams")

class MaintenanceTicket(models.Model):
    equipment = models.ForeignKey(Equipment, on_delete=models.CASCADE)
    description = models.CharField(
        max_length=500, unique=False, default="", editable=True)
    issue_date = models.DateField(auto_now_add=True)
    resolution_date = models.DateField(null=True, blank=True)
    # raiser = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    raised_by = models.ForeignKey(
        User, blank=True, null=True, on_delete=models.DO_NOTHING)
    teams = models.ManyToManyField(Team, related_name="teams_required")
    # when a team assigns one of its coordinators to the task it will be stored here
    teams_responded = models.ManyToManyField(
        Team, related_name="teams_responded")
    technician_assigned = models.ManyToManyField(
        User,null=True, blank=True, related_name="tech_assigned")
    technician_completed = models.ManyToManyField(
        User, blank=True, null=True, related_name="tech_completed")
    status = models.CharField(
        max_length=10, default="raised", editable=True)


class UserRequest(models.Model):
    name = models.CharField(max_length=100, null=False,
                            blank=False, default="", editable=True)
    email = models.EmailField(unique=True)
    department = models.ForeignKey(
        Department,  on_delete=models.CASCADE, null=True)
    designation = models.CharField(
        max_length=5, unique=False, default="", editable=True)
    date_raised = models.DateField(auto_now_add=True)
    status = models.CharField(
        max_length=10, default="raised", editable=True)
