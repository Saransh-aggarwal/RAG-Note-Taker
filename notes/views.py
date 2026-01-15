from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm

class NoteListView(LoginRequiredMixin, View):
    """Display list of user's notes with search functionality."""
    template_name = 'notes/note_list.html'

    def get(self, request):
        query = request.GET.get('q')
        notes = Note.objects.filter(user=request.user, is_deleted=False)
        
        if query:
            notes = notes.filter(
                Q(title__icontains=query) | 
                Q(content__icontains=query)
            )

        return render(request, self.template_name, {
            'notes': notes,
            'search_query': query or ''
        })

class NoteCreateView(LoginRequiredMixin, View):
    """Create a new note."""
    template_name = 'notes/note_form.html'

    def get(self, request):
        form = NoteForm()
        return render(request, self.template_name, {'form': form, 'action': 'Create'})

    def post(self, request):
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, "Note created successfully.")
            return redirect('notes:list')
        
        return render(request, self.template_name, {'form': form, 'action': 'Create'})

class NoteDetailView(LoginRequiredMixin, View):
    """View a single note."""
    template_name = 'notes/note_detail.html'

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user, is_deleted=False)
        return render(request, self.template_name, {'note': note})

class NoteUpdateView(LoginRequiredMixin, View):
    """Update an existing note."""
    template_name = 'notes/note_form.html'

    def get(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user, is_deleted=False)
        form = NoteForm(instance=note)
        return render(request, self.template_name, {'form': form, 'action': 'Update', 'note': note})

    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user, is_deleted=False)
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, "Note updated successfully.")
            return redirect('notes:detail', pk=pk)
        
        return render(request, self.template_name, {'form': form, 'action': 'Update', 'note': note})

class NoteDeleteView(LoginRequiredMixin, View):
    """Soft delete a note."""
    
    def post(self, request, pk):
        note = get_object_or_404(Note, pk=pk, user=request.user)
        note.soft_delete()
        messages.success(request, "Note deleted successfully.")
        return redirect('notes:list')
