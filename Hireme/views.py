from django.shortcuts import render
from jobs.models import Job

def home(request):
    recent_jobs = Job.objects.filter(status='active').order_by('-created_at')[:3]
    return render(request, 'home.html', {'recent_jobs': recent_jobs})
