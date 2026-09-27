from django.shortcuts import render
from django.utils import timezone
from datetime import timedelta
from tasks.models import Task
from notes.models import Note
from learning.models import Skill, Topic

def home(request):
    """
    Renders SaaS Landing Page for guests,
    or Student Dashboard workspace for authenticated users.
    """
    if request.user.is_authenticated:
        today = timezone.now().date()
        tasks = Task.objects.filter(user=request.user)
        notes = Note.objects.filter(user=request.user)
        skills = Skill.objects.filter(user=request.user)
        topics = Topic.objects.filter(skill__user=request.user)

        total_tasks = tasks.count()
        completed_tasks = tasks.filter(status='COMPLETED').count()
        pending_tasks_count = total_tasks - completed_tasks

        # Strict filter for Today's Tasks by due_date == today
        today_tasks = tasks.filter(due_date=today)
        today_tasks_count = today_tasks.count()
        today_high_prio_count = today_tasks.filter(priority='HIGH').exclude(status='COMPLETED').count()
        today_pending_count = today_tasks.exclude(status='COMPLETED').count()

        # Process Skills and annotate next_topic_title
        active_skills_list = []
        for s in skills[:4]:
            next_tp = s.topics.exclude(status='COMPLETED').order_by('order', 'created_at').first()
            if next_tp:
                next_title = f"Next: {next_tp.title}"
            elif s.total_topics_count > 0:
                next_title = "All Topics Mastered! 🎉"
            else:
                next_title = "Add topics to start"
            
            s.next_topic_title = next_title
            active_skills_list.append(s)

        total_notes = notes.count()
        total_skills = skills.count()
        completed_topics_count = topics.filter(status='COMPLETED').count()

        # Compute Weekly Momentum Graph based on 7-day real activity dataset (Tasks, Notes, & Skills)
        start_date = today - timedelta(days=6)
        weekly_momentum = []
        total_weekly_activity = 0

        daily_counts = []
        for i in range(7):
            day_date = start_date + timedelta(days=i)

            # Task activity on day_date
            t_created = tasks.filter(created_at__date=day_date).count()
            t_completed = tasks.filter(updated_at__date=day_date, status='COMPLETED').count()
            task_act = t_created + t_completed

            # Note activity on day_date
            n_created = notes.filter(created_at__date=day_date).count()
            n_updated = notes.filter(updated_at__date=day_date).exclude(created_at__date=day_date).count()
            note_act = n_created + n_updated

            # Skill & Topic learning activity on day_date
            tp_created = topics.filter(created_at__date=day_date).count()
            tp_learned = topics.filter(date_learned=day_date).count()
            tp_completed = topics.filter(updated_at__date=day_date, status='COMPLETED').count()
            skill_act = tp_created + tp_learned + tp_completed

            day_total = task_act + note_act + skill_act
            daily_counts.append({
                'date': day_date,
                'task_act': task_act,
                'note_act': note_act,
                'skill_act': skill_act,
                'total': day_total
            })

        max_val = max([d['total'] for d in daily_counts]) if daily_counts else 0
        grid_max = max(max_val, 4)
        grid_labels = [grid_max, round(grid_max * 0.75), round(grid_max * 0.5), round(grid_max * 0.25), 0]

        for i, d in enumerate(daily_counts):
            day_date = d['date']
            val = d['total']
            total_weekly_activity += val
            
            if val > 0:
                height_pct = max(6, int(round((val / grid_max) * 100)))
            else:
                height_pct = 0

            weekly_momentum.append({
                'day_label': 'Today' if day_date == today else day_date.strftime('%a'),
                'full_date': day_date.strftime('%b %d'),
                'val': val,
                'task_act': d['task_act'],
                'note_act': d['note_act'],
                'skill_act': d['skill_act'],
                'height_pct': height_pct,
                'is_today': day_date == today,
            })

        context = {
            'today': today,
            'total_tasks': total_tasks,
            'completed_tasks': completed_tasks,
            'pending_tasks_count': pending_tasks_count,
            'today_tasks': today_tasks,
            'today_tasks_count': today_tasks_count,
            'today_high_prio_count': today_high_prio_count,
            'today_pending_count': today_pending_count,
            'total_notes': total_notes,
            'total_skills': total_skills,
            'completed_topics_count': completed_topics_count,
            'skills': active_skills_list,
            'weekly_momentum': weekly_momentum,
            'total_weekly_activity': total_weekly_activity,
            'grid_labels': grid_labels,
            'active_tab': 'dashboard',
        }
        return render(request, 'dashboard.html', context)

    # Guest Landing Page
    return render(request, 'home.html', {'active_tab': 'home'})
