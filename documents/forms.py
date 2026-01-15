from django import forms
from .models import Document


class DocumentUploadForm(forms.ModelForm):
    """Form for uploading documents."""

    class Meta:
        model = Document
        fields = ['file']

    def clean_file(self):
        file = self.cleaned_data.get('file')
        if file:
            # Check file extension
            ext = file.name.split('.')[-1].lower()
            allowed_extensions = ['pdf', 'txt', 'docx']
            if ext not in allowed_extensions:
                raise forms.ValidationError(
                    f"Unsupported file type. Allowed: {', '.join(allowed_extensions)}"
                )

            # Check file size (10MB limit)
            if file.size > 10 * 1024 * 1024:
                raise forms.ValidationError("File size must be under 10MB.")

        return file
