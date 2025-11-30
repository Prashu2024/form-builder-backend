from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from django.core.paginator import Paginator
from .models import FormSubmission
from .serializers import FormSubmissionSerializer
from .validators import FormValidator

# Employee Onboarding Form Schema
FORM_SCHEMA = {
    "title": "Employee Onboarding Form",
    "description": "Please fill out this form to complete your onboarding process.",
    "fields": [
        {
            "name": "fullName",
            "type": "text",
            "label": "Full Name",
            "placeholder": "Enter your full name",
            "required": True,
            "validation": {
                "minLength": 2,
                "maxLength": 100
            }
        },
        {
            "name": "email",
            "type": "text",
            "label": "Email Address",
            "placeholder": "your.email@company.com",
            "required": True,
            "validation": {
                "regex": "^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}$",
                "regexMessage": "Please enter a valid email address"
            }
        },
        {
            "name": "age",
            "type": "number",
            "label": "Age",
            "placeholder": "Enter your age",
            "required": True,
            "validation": {
                "min": 18,
                "max": 100
            }
        },
        {
            "name": "department",
            "type": "select",
            "label": "Department",
            "placeholder": "Select your department",
            "required": True,
            "options": [
                {"label": "Engineering", "value": "engineering"},
                {"label": "Marketing", "value": "marketing"},
                {"label": "Sales", "value": "sales"},
                {"label": "Human Resources", "value": "hr"},
                {"label": "Finance", "value": "finance"}
            ]
        },
        {
            "name": "skills",
            "type": "multi-select",
            "label": "Technical Skills",
            "placeholder": "Select your skills (hold Ctrl/Cmd to select multiple)",
            "required": True,
            "options": [
                {"label": "JavaScript", "value": "javascript"},
                {"label": "Python", "value": "python"},
                {"label": "Java", "value": "java"},
                {"label": "React", "value": "react"},
                {"label": "Django", "value": "django"},
                {"label": "SQL", "value": "sql"}
            ],
            "validation": {
                "minSelected": 1,
                "maxSelected": 4
            }
        },
        {
            "name": "startDate",
            "type": "date",
            "label": "Start Date",
            "placeholder": "Select your start date",
            "required": True,
            "validation": {
                "minDate": "2024-01-01"
            }
        },
        {
            "name": "bio",
            "type": "textarea",
            "label": "Brief Bio",
            "placeholder": "Tell us about yourself...",
            "required": False,
            "validation": {
                "maxLength": 500
            }
        },
        {
            "name": "agreeToTerms",
            "type": "switch",
            "label": "Terms and Conditions",
            "placeholder": "I agree to the terms and conditions",
            "required": True
        }
    ]
}

@api_view(['GET'])
def get_form_schema(request):
    """GET /api/form-schema - Returns the form schema"""
    return Response(FORM_SCHEMA, status=status.HTTP_200_OK)


@api_view(['GET', 'POST'])
def submissions_view(request):
    """
    GET /api/submissions - Get paginated and sorted submissions
    POST /api/submissions - Create a new form submission
    """
    if request.method == 'POST':
        try:
            # Validate against schema
            validator = FormValidator(FORM_SCHEMA)
            validator.validate(request.data)
            
            # Create submission
            submission = FormSubmission.objects.create(data=request.data)
            serializer = FormSubmissionSerializer(submission)
            
            return Response({
                'success': True,
                'id': str(submission.id),
                'createdAt': submission.created_at.isoformat(),
                'data': serializer.data
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            if hasattr(e, 'detail'):
                return Response({
                    'success': False,
                    'errors': e.detail
                }, status=status.HTTP_400_BAD_REQUEST)
            
            return Response({
                'success': False,
                'errors': {'general': str(e)}
            }, status=status.HTTP_400_BAD_REQUEST)
    
    else:  # GET request
        try:
            # Get query parameters
            page = int(request.GET.get('page', 1))
            limit = int(request.GET.get('limit', 10))
            sort_by = request.GET.get('sortBy', 'createdAt')
            sort_order = request.GET.get('sortOrder', 'desc')
            
            # Validate parameters
            if page < 1:
                page = 1
            if limit not in [10, 20, 50]:
                limit = 10
            
            # Get all submissions
            queryset = FormSubmission.objects.all()
            
            # Apply sorting
            if sort_by == 'createdAt':
                if sort_order == 'asc':
                    queryset = queryset.order_by('created_at')
                else:
                    queryset = queryset.order_by('-created_at')
            
            # Paginate
            paginator = Paginator(queryset, limit)
            page_obj = paginator.get_page(page)
            
            # Serialize submissions
            submissions = []
            for submission in page_obj:
                submissions.append({
                    'id': str(submission.id),
                    'createdAt': submission.created_at.isoformat(),
                    **submission.data
                })
            
            return Response({
                'submissions': submissions,
                'total': paginator.count,
                'page': page,
                'limit': limit,
                'totalPages': paginator.num_pages
            }, status=status.HTTP_200_OK)
            
        except Exception as e:
            return Response({
                'error': str(e)
            }, status=status.HTTP_400_BAD_REQUEST)
