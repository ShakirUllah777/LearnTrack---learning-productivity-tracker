from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from .models import Note
from .forms import NoteForm

@login_required
def note_list(request):
    query = request.GET.get('q', '').strip()
    tag_filter = request.GET.get('tag', '').strip()

    all_user_notes = Note.objects.filter(user=request.user)

    # Extract unique tags across all user notes
    all_tags = set()
    for n in all_user_notes:
        for t in n.tag_list:
            all_tags.add(t)
    all_tags = sorted(list(all_tags))

    notes = all_user_notes

    if query:
        notes = notes.filter(Q(title__icontains=query) | Q(content__icontains=query) | Q(tags__icontains=query))
    if tag_filter:
        notes = notes.filter(tags__icontains=tag_filter)

    form = NoteForm()
    context = {
        'notes': notes,
        'all_tags': all_tags,
        'form': form,
        'query': query,
        'tag_filter': tag_filter,
        'active_tab': 'notes',
    }
    return render(request, 'notes/note_list.html', context)


@login_required
def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = request.user
            note.save()
            messages.success(request, f"Note '{note.title}' created successfully!")
        else:
            messages.error(request, "Failed to create note. Please check form fields.")
    return redirect('note_list')


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            form.save()
            messages.success(request, f"Note '{note.title}' updated successfully!")
            return redirect('note_list')
        else:
            messages.error(request, "Failed to update note.")
    else:
        form = NoteForm(instance=note)

    return render(request, 'notes/note_edit.html', {'form': form, 'note': note, 'active_tab': 'notes'})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk, user=request.user)
    if request.method == 'POST':
        title = note.title
        note.delete()
        messages.success(request, f"Note '{title}' deleted.")
    return redirect('note_list')
