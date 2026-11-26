from django.contrib import admin

from .models import Appointment


@admin.action(description='Make them confirmed')
def Confirmed_appointment(model, req, queryset):
    queryset.update(status='CONFIRMED')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    actions = [Confirmed_appointment,]
    list_display = ('reason', 'status', 'duration_minutes', 'appointment_date', 'doctor', 'patient')
    list_filter = ('status', 'appointment_date')
    list_editable = ('status',)
    search_fields = ('reason', 'status')
    ordering = ('appointment_date',)
    fieldsets = (
        ('Description',{ 
            "fields":('reason' , 'status','prescription')
        }),
        ('Date + Duration',{
            "fields":('appointment_date' , 'duration_minutes')
            }),
        ('Patient/Doctor',{
            "fields":('doctor' , 'patient')
        }),
        ('planification',{
            "fields":('created_at' , 'updated_at')
        }),
    )
    readonly_fields = ('created_at', 'updated_at')

