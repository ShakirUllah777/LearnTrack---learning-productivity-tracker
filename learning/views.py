from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Skill, Topic
from .forms import SkillForm, TopicForm

@login_required
def skill_list(request):
    skills = Skill.objects.filter(user=request.user)
    form = SkillForm()
    context = {
        'skills': skills,
        'form': form,
        'active_tab': 'learning',
    }
    return render(request, 'learning/skill_list.html', context)


@login_required
def skill_create(request):
    if request.method == 'POST':
        form = SkillForm(request.POST)
        if form.is_valid():
            skill = form.save(commit=False)
            skill.user = request.user
            skill.save()
            messages.success(request, f"Skill '{skill.name}' created successfully!")
            return redirect('skill_detail', pk=skill.pk)
        else:
            messages.error(request, "Failed to create skill. Check the form.")
    return redirect('skill_list')


@login_required
def skill_edit(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SkillForm(request.POST, instance=skill)
        if form.is_valid():
            form.save()
            messages.success(request, f"Skill '{skill.name}' updated.")
            return redirect('skill_detail', pk=skill.pk)
        else:
            messages.error(request, "Failed to update skill.")
    else:
        form = SkillForm(instance=skill)
    return render(request, 'learning/skill_edit.html', {'form': form, 'skill': skill, 'active_tab': 'learning'})


@login_required
def skill_delete(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    if request.method == 'POST':
        name = skill.name
        skill.delete()
        messages.success(request, f"Skill '{name}' deleted.")
    return redirect('skill_list')


@login_required
def skill_detail(request, pk):
    skill = get_object_or_404(Skill, pk=pk, user=request.user)
    topics = skill.topics.all()
    
    # Pre-fill order for new topic form
    next_order = topics.count() + 1
    topic_form = TopicForm(initial={'order': next_order})
    skill_form = SkillForm(instance=skill)

    context = {
        'skill': skill,
        'topics': topics,
        'topic_form': topic_form,
        'skill_form': skill_form,
        'active_tab': 'learning',
    }
    return render(request, 'learning/skill_detail.html', context)


@login_required
def topic_create(request, skill_pk):
    skill = get_object_or_404(Skill, pk=skill_pk, user=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.skill = skill
            topic.save()
            messages.success(request, f"Topic '{topic.title}' added to {skill.name}!")
        else:
            messages.error(request, "Failed to add topic. Check form errors.")
    return redirect('skill_detail', pk=skill.pk)


@login_required
def topic_edit(request, pk):
    topic = get_object_or_404(Topic, pk=pk, skill__user=request.user)
    if request.method == 'POST':
        form = TopicForm(request.POST, instance=topic)
        if form.is_valid():
            form.save()
            messages.success(request, f"Topic '{topic.title}' updated.")
            return redirect('skill_detail', pk=topic.skill.pk)
    else:
        form = TopicForm(instance=topic)
    return render(request, 'learning/topic_edit.html', {'form': form, 'topic': topic, 'active_tab': 'learning'})


@login_required
def topic_delete(request, pk):
    topic = get_object_or_404(Topic, pk=pk, skill__user=request.user)
    skill_pk = topic.skill.pk
    if request.method == 'POST':
        title = topic.title
        topic.delete()
        messages.success(request, f"Topic '{title}' deleted.")
    return redirect('skill_detail', pk=skill_pk)


@login_required
def topic_toggle(request, pk):
    topic = get_object_or_404(Topic, pk=pk, skill__user=request.user)
    if topic.status == 'NOT_STARTED':
        topic.status = 'CURRENTLY_LEARNING'
    elif topic.status == 'CURRENTLY_LEARNING':
        topic.status = 'COMPLETED'
    else:
        topic.status = 'NOT_STARTED'
    topic.save()
    messages.success(request, f"Status of topic '{topic.title}' updated.")
    return redirect('skill_detail', pk=topic.skill.pk)
