from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta

User = get_user_model()


class ChatMessage(models.Model):
    """
    Represents a single chat message in a conversation.
    Only messages from the last 24 hours are considered for context.
    """
    ROLE_CHOICES = [
        ('user', 'User'),
        ('assistant', 'Assistant'),
    ]

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='chat_messages',
        help_text="The user this message belongs to"
    )
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        help_text="Whether this is a user message or assistant response"
    )
    content = models.TextField(
        help_text="The message content"
    )
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        ordering = ['created_at']
        indexes = [
            models.Index(fields=['user', 'created_at']),
        ]

    def __str__(self):
        preview = self.content[:50] + '...' if len(self.content) > 50 else self.content
        return f"{self.role}: {preview}"

    @classmethod
    def get_recent_history(cls, user, hours=24):
        """
        Returns messages from the last N hours for a user.
        This is the core mechanism for the 24-hour memory window.
        """
        cutoff_time = timezone.now() - timedelta(hours=hours)
        return cls.objects.filter(
            user=user,
            created_at__gte=cutoff_time
        ).order_by('created_at')

    @classmethod
    def get_history_for_context(cls, user, hours=24, max_messages=20):
        """
        Returns formatted history suitable for LLM context.
        Limits to most recent N messages to avoid context overflow.
        """
        messages = cls.get_recent_history(user, hours)[:max_messages]
        return [
            {'role': msg.role, 'content': msg.content}
            for msg in messages
        ]
