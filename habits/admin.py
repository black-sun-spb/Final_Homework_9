from django.contrib import admin
from .models import Habit


# --- Привычки ---
@admin.register(Habit)
class HabitAdmin(admin.ModelAdmin):
    list_display = ("owner", "action", "time", "is_rewarding", "is_public")
    search_fields = ("action", "owner__username")
    list_filter = ("is_rewarding", "is_public", "periodicity_days")
