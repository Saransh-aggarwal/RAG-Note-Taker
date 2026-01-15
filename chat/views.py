import json
from django.shortcuts import render
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.http import JsonResponse

from .models import ChatMessage
from documents.models import Document
from rag.services import rag_service


class ChatView(LoginRequiredMixin, View):
    """Main chat interface."""
    template_name = 'chat/chat.html'

    def get(self, request):
        # Get user's active documents for selection
        documents = Document.get_active_for_user(request.user)

        # Get recent chat history (last 24 hours)
        chat_messages = ChatMessage.get_recent_history(request.user, hours=24)

        return render(request, self.template_name, {
            'documents': documents,
            'chat_messages': chat_messages,
        })


class ChatAPIView(LoginRequiredMixin, View):
    """API endpoint for chat messages (AJAX)."""

    def post(self, request):
        try:
            data = json.loads(request.body)
            question = data.get('message', '').strip()
            selected_doc_ids = data.get('document_ids', [])

            if not question:
                return JsonResponse({
                    'success': False,
                    'error': 'Please enter a message.'
                }, status=400)

            if not selected_doc_ids:
                return JsonResponse({
                    'success': False,
                    'error': 'Please select at least one document.'
                }, status=400)

            # Validate document ownership
            user_docs = Document.get_active_for_user(request.user)
            valid_doc_ids = list(user_docs.filter(id__in=selected_doc_ids).values_list('id', flat=True))

            if not valid_doc_ids:
                return JsonResponse({
                    'success': False,
                    'error': 'Selected documents are not available.'
                }, status=400)

            # Save user message
            user_message = ChatMessage.objects.create(
                user=request.user,
                role='user',
                content=question
            )

            # Get chat history for context
            history = ChatMessage.get_history_for_context(request.user, hours=24, max_messages=10)

            # Get answer from RAG service
            answer = rag_service.answer_question(
                question=question,
                user_id=request.user.id,
                selected_document_ids=valid_doc_ids,
                chat_history=history
            )

            # Save assistant response
            assistant_message = ChatMessage.objects.create(
                user=request.user,
                role='assistant',
                content=answer
            )

            return JsonResponse({
                'success': True,
                'message': {
                    'role': 'assistant',
                    'content': answer,
                    'created_at': assistant_message.created_at.isoformat(),
                }
            })

        except json.JSONDecodeError:
            return JsonResponse({
                'success': False,
                'error': 'Invalid request format.'
            }, status=400)
        except Exception as e:
            return JsonResponse({
                'success': False,
                'error': f'An error occurred: {str(e)}'
            }, status=500)


class ClearHistoryView(LoginRequiredMixin, View):
    """Clear chat history for current user."""

    def post(self, request):
        ChatMessage.objects.filter(user=request.user).delete()
        return JsonResponse({'success': True})
