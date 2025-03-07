from django.contrib import admin
from django.db.models import Window, F
from django.db.models.functions import Rank
from .models import Contestant
import pandas as pd
from django.http import HttpResponse





@admin.action(description="Export selected contestants to Excel")
def export_to_excel(modeladmin, request, queryset):
    """Export queryset data to an Excel file."""
    # Annotate ranks dynamically
    queryset = queryset.annotate(
        rank=Window(expression=Rank(), order_by=F('total_marks').desc())
    )

    # Convert to DataFrame
    data = list(queryset.values('email', 'total_marks', 'rank'))  # Add needed fields
    df = pd.DataFrame(data)

    # Create a response object for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="contestants.xlsx"'

    # Save DataFrame to Excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response

@admin.register(Contestant)
class ContestantAdmin(admin.ModelAdmin):
    list_display = ('get_position', 'email', 'total_marks')  
    ordering = ('-total_marks',)  

    def get_queryset(self, request):
        """Use Window function to assign rank based on total_marks."""
        return super().get_queryset(request).annotate(
            rank=Window(expression=Rank(), order_by=F('total_marks').desc())
        )

    def get_position(self, obj):
        """Return the annotated rank."""
        return obj.rank

    get_position.admin_order_field = 'rank'  
    get_position.short_description = "Position"
