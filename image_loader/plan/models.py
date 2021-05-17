from django.db import models
from django.contrib.auth.models import User


class Plan(models.Model):
    """
    Each Plan has specified allowed sizes (height)
    Allowed sizes are separeted by spaces
    """

    plan_name = models.CharField(max_length=20)
    allowed_sizes = models.CharField(max_length=255, default="200")
    acces_to_the_og = models.BooleanField(default=False)
    ability_to_generate_expiring_links = models.BooleanField(default=False)

    def __str__(self):
        return self.plan_name

    def get_allowed_sizes(self):
        return allowed_sizes.split()


class UserPlan(models.Model):
    """
    Every Client has his own Plan
    """

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="userplan_user"
    )
    plan = models.ForeignKey(
        Plan, on_delete=models.CASCADE, related_name="userplan_plan"
    )

    def __str__(self):
        return f"{self.user} || {self.plan}"