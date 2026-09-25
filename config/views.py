from django.shortcuts import render
from tasks.models import Task
from notes.models import Note
from learning.models import Skill

def home(request):
    """
    Renders SaaS Landing Page for guests,
    or Student Dashboard workspace for authenticated users.
    """
    if request.user.is_authenticated:
        tasks = Task.objects.filter(user=request.user)
        notes = Note.objects.filter(user=request.user)
        skills = Skill.objects.filter(user=request.user)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='COMPLETED').count()
        pending_tasks = tasks.exclude(status='COMPLETED')[:5]

        total_notes = notes.count()
        recent_notes = notes[:3]

        total_skills = skills.count()

        context = {
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks': pending_tasks,
            'total_notes': total_notes,
            'recent_notes': recent_notes,
            'total_skills': total_skills,
            'skills': skills[:4],
            'active_tab': 'dashboard',
        }
        return render(request, 'dashboard.html', context)

    # Guest Landing Page
    return render(request, 'home.html', {'active_tab': 'home'})
