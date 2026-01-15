from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views import View


from .models import Document
from .forms import DocumentUploadForm
from rag.services import rag_service


class DocumentListView(LoginRequiredMixin, View):
    """Display list of user's documents."""
    template_name = 'documents/list.html'

    def get(self, request):
        documents = Document.get_active_for_user(request.user)
        form = DocumentUploadForm()
        return render(request, self.template_name, {
            'documents': documents,
            'form': form,
        })


class DocumentUploadView(LoginRequiredMixin, View):
    """Handle document upload and indexing."""

    def post(self, request):
        files = request.FILES.getlist('file')
        if not files:
            messages.error(request, "No files selected.")
            return redirect('documents:list')

        success_count = 0
        fail_count = 0

        for file in files:
            # Basic validation (similar to form)
            ext = file.name.split('.')[-1].lower()
            if ext not in ['pdf', 'txt', 'docx']:
                messages.error(request, f"File '{file.name}' has an unsupported type.")
                fail_count += 1
                continue
            
            if file.size > 10 * 1024 * 1024:
                messages.error(request, f"File '{file.name}' exceeds the 10MB limit.")
                fail_count += 1
                continue

            try:
                document = Document(
                    user=request.user,
                    file=file,
                    name=file.name
                )
                document.save()

                # Index the document in ChromaDB
                success = rag_service.index_document(document, request.user.id)
                if success:
                    document.is_indexed = True
                    document.save()
                    success_count += 1
                else:
                    fail_count += 1
                    messages.warning(request, f"Indexing failed for '{file.name}'.")
            except Exception as e:
                fail_count += 1
                messages.error(request, f"Error uploading '{file.name}': {str(e)}")

        if success_count > 0:
            messages.success(request, f"Successfully uploaded and indexed {success_count} document(s).")
        
        if fail_count > 0:
            messages.info(request, f"Failed to process {fail_count} document(s).")

        return redirect('documents:list')


class DocumentDeleteView(LoginRequiredMixin, View):
    """Soft delete a document."""

    def post(self, request, pk):
        document = get_object_or_404(Document, pk=pk, user=request.user)

        # Soft delete
        document.is_deleted = True
        document.save()

        # Remove embeddings from ChromaDB
        rag_service.delete_document_embeddings(document.id, request.user.id)

        messages.success(request, f"'{document.name}' has been deleted.")
        return redirect('documents:list')
