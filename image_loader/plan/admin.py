from django.contrib import admin
from image_loader.plan.models import Plan, UserPlan


@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    """
    Custom Admin Model for Plan Model
    """

    model = Plan
    search_fields = (
        "plan_name",
        "ability_to_generate_expiring_links",
        "acces_to_the_og",
    )
    list_filter = ("plan_name", "ability_to_generate_expiring_links", "acces_to_the_og")
    ordering = ("plan_name", "ability_to_generate_expiring_links", "acces_to_the_og")
    list_display = (
        "plan_name",
        "ability_to_generate_expiring_links",
        "acces_to_the_og",
        "allowed_sizes",
    )
    fieldsets = (
        (
            "Info",
            {
                "fields": (
                    "plan_name",
                    "ability_to_generate_expiring_links",
                    "acces_to_the_og",
                    "allowed_sizes",
                )
            },
        ),
    )


@admin.register(UserPlan)
class UserPlanAdmin(admin.ModelAdmin):
    """
    Custom Admin Model for UserPlan Model
    """

    model = UserPlan
    search_fields = ('user', 'plan')
    list_display = ('user', 'plan')