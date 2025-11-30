from rest_framework import serializers
from .models import FormSubmission

class FormSubmissionSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)
    
    class Meta:
        model = FormSubmission
        fields = ['id', 'data', 'createdAt']
        read_only_fields = ['id', 'createdAt']