from django.shortcuts import render
import pandas as pd
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from .models import Contestant
from django.db import transaction
from .serializers import ContestantSerializer,FileUploadSerializer
from django.db.models import Window, F
from django.db.models.functions import Rank
from django.http import HttpResponse


class UploadLeaderboardView(APIView):
    parser_classes = [MultiPartParser, FormParser]
    serializer_class = FileUploadSerializer

    def post(self, request, *args, **kwargs):
        serializer = FileUploadSerializer(data=request.data)  # Use serializer

        if serializer.is_valid():
            file = serializer.validated_data['file']

            try:
                df = pd.read_excel(file)  # Read Excel file
                
                with transaction.atomic():  # Ensure atomic updates
                    for _, row in df.iterrows():
                        name = str(row["Identity"]).strip().lower()
                        marks = int(row["marks"])

                        contestant, created = Contestant.objects.get_or_create(email=name)
                        contestant.total_marks += marks
                        contestant.save()
                
                return Response({"message": "Leaderboard updated successfully"}, status=status.HTTP_200_OK)
            
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LeaderboardView(ListAPIView):
    queryset = Contestant.objects.order_by('-total_marks')
    serializer_class = ContestantSerializer


def export_contestants_to_excel(request):
    """Export contestants with dynamic ranks to an Excel file."""
    # Annotate rank dynamically
    queryset = Contestant.objects.annotate(
        rank=Window(expression=Rank(), order_by=F('total_marks').desc())
    ).values('email', 'total_marks', 'rank')  # Select required fields

    if not queryset.exists():
        return HttpResponse("No data available to export.", content_type="text/plain")

    # Convert queryset to DataFrame
    df = pd.DataFrame(list(queryset))

    # Create a response object for Excel
    response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
    response['Content-Disposition'] = 'attachment; filename="contestants.xlsx"'

    # Save DataFrame to Excel
    df.to_excel(response, index=False, engine='openpyxl')

    return response
