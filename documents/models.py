from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Document(models.Model):
    """
    Represents a user-uploaded document for RAG indexing.
    Supports soft delete - documents are never physically removed in V1.
    """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='documents',
        help_text="The user who uploaded this document"
    )
    name = models.CharField(
        max_length=255,
        help_text="Original filename of the document"
    )
    file = models.FileField(
        upload_to='documents/%Y/%m/%d/',
        help_text="Path to the uploaded file"
    )
    is_deleted = models.BooleanField(
        default=False,
        db_index=True,
        help_text="Soft delete flag - if True, document is hidden from user"
    )
    is_indexed = models.BooleanField(
        default=False,
        help_text="Whether the document has been successfully indexed in ChromaDB"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['user', 'is_deleted']),
        ]

    def __str__(self):
        return f"{self.name} ({self.user.username})"

    @property
    def file_extension(self):
        """Returns the file extension in lowercase."""
        return self.name.split('.')[-1].lower() if '.' in self.name else ''

    @classmethod
    def get_active_for_user(cls, user):
        """Returns all non-deleted documents for a user."""
        return cls.objects.filter(user=user, is_deleted=False)
