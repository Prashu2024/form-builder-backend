import re
from datetime import datetime
from rest_framework.exceptions import ValidationError

class FormValidator:
    def __init__(self, schema):
        self.schema = schema
        self.errors = {}
    
    def validate(self, data):
        """Validate form data against schema"""
        for field in self.schema['fields']:
            field_name = field['name']
            field_value = data.get(field_name)
            
            # Check required fields
            if field.get('required') and not self._has_value(field_value):
                self.errors[field_name] = f"{field['label']} is required"
                continue
            
            # Skip validation if field is not required and empty
            if not self._has_value(field_value):
                continue
            
            # Type-specific validation
            if field['type'] == 'text':
                self._validate_text(field_name, field_value, field)
            elif field['type'] == 'number':
                self._validate_number(field_name, field_value, field)
            elif field['type'] == 'select':
                self._validate_select(field_name, field_value, field)
            elif field['type'] == 'multi-select':
                self._validate_multi_select(field_name, field_value, field)
            elif field['type'] == 'date':
                self._validate_date(field_name, field_value, field)
            elif field['type'] == 'textarea':
                self._validate_text(field_name, field_value, field)
            elif field['type'] == 'switch':
                self._validate_switch(field_name, field_value, field)
        
        if self.errors:
            raise ValidationError(self.errors)
        
        return True
    
    def _has_value(self, value):
        """Check if value exists and is not empty"""
        if value is None:
            return False
        if isinstance(value, str) and not value.strip():
            return False
        if isinstance(value, list) and len(value) == 0:
            return False
        return True
    
    def _validate_text(self, name, value, field):
        """Validate text fields"""
        validation = field.get('validation', {})
        
        if validation.get('minLength') and len(value) < validation['minLength']:
            self.errors[name] = f"Minimum {validation['minLength']} characters required"
        
        if validation.get('maxLength') and len(value) > validation['maxLength']:
            self.errors[name] = f"Maximum {validation['maxLength']} characters allowed"
        
        if validation.get('regex'):
            pattern = validation['regex']
            if not re.match(pattern, value):
                self.errors[name] = validation.get('regexMessage', 'Invalid format')
    
    def _validate_number(self, name, value, field):
        """Validate number fields"""
        try:
            num_value = float(value)
        except (ValueError, TypeError):
            self.errors[name] = "Must be a valid number"
            return
        
        validation = field.get('validation', {})
        
        if validation.get('min') is not None and num_value < validation['min']:
            self.errors[name] = f"Minimum value is {validation['min']}"
        
        if validation.get('max') is not None and num_value > validation['max']:
            self.errors[name] = f"Maximum value is {validation['max']}"
    
    def _validate_select(self, name, value, field):
        """Validate select fields"""
        valid_options = [opt['value'] for opt in field.get('options', [])]
        if value not in valid_options:
            self.errors[name] = "Invalid selection"
    
    def _validate_multi_select(self, name, value, field):
        """Validate multi-select fields"""
        if not isinstance(value, list):
            self.errors[name] = "Must be a list of values"
            return
        
        valid_options = [opt['value'] for opt in field.get('options', [])]
        for v in value:
            if v not in valid_options:
                self.errors[name] = "Invalid selection"
                return
        
        validation = field.get('validation', {})
        
        if validation.get('minSelected') and len(value) < validation['minSelected']:
            self.errors[name] = f"Select at least {validation['minSelected']} option(s)"
        
        if validation.get('maxSelected') and len(value) > validation['maxSelected']:
            self.errors[name] = f"Select at most {validation['maxSelected']} option(s)"
    
    def _validate_date(self, name, value, field):
        """Validate date fields"""
        try:
            date_value = datetime.fromisoformat(value.replace('Z', '+00:00'))
        except (ValueError, AttributeError):
            self.errors[name] = "Invalid date format"
            return
        
        validation = field.get('validation', {})
        
        if validation.get('minDate'):
            min_date = datetime.fromisoformat(validation['minDate'])
            if date_value < min_date:
                self.errors[name] = f"Date must be after {validation['minDate']}"
    
    def _validate_switch(self, name, value, field):
        """Validate switch fields"""
        if not isinstance(value, bool):
            self.errors[name] = "Must be a boolean value"
