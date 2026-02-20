from django.shortcuts import render, redirect
from .models import Job, Application, Category
from django.contrib.auth.decorators import login_required
from users.decorators import hr_required

from .forms import JobForm

@login_required
@hr_required
def post_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user
            job.status = 'active' # Auto-approve jobs posted by HR

            # Handle new category
            new_category_name = form.cleaned_data.get('new_category')
            if new_category_name:
                category, created = Category.objects.get_or_create(name__iexact=new_category_name, defaults={'name': new_category_name})
                job.category = category

            job.save()
            return redirect('job_list')
    else:
        form = JobForm()
    return render(request, 'post_job.html', {'form': form})

from django.db.models import Q

def job_list(request):
    jobs = Job.objects.filter(status='active').order_by('-created_at')
    
    
    # Filter by Category
    category_id = request.GET.get('category')
    if category_id:
        jobs = jobs.filter(category_id=category_id)

    # Search Filter
    query = request.GET.get('q')
    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(location__icontains=query) | Q(category__name__icontains=query))

    # Recommendations (Skill Matching)
    # ... (keeping existing logic for now, but ensure it works with filtered jobs)
    if request.user.is_authenticated and hasattr(request.user, 'userprofile') and request.user.userprofile.skills:
        user_skills = [s.strip().lower() for s in request.user.userprofile.skills.split(',') if s.strip()]
        
        # Calculate match score for each job
        # Note: This is a simple Python-side implementation. For production, DB-level matching is better.
        job_list_with_scores = []
        for job in jobs:
            job_skills = [s.strip().lower() for s in job.skills_required.split(',') if s.strip()]
            match_count = sum(1 for skill in user_skills if skill in job_skills)
            job.match_score = match_count
            job_list_with_scores.append(job)
            
        # Sort by match score (descending) then by creation date (descending)
        jobs = sorted(job_list_with_scores, key=lambda x: (x.match_score, x.created_at), reverse=True)

    applied_job_ids = []
    if request.user.is_authenticated and not hasattr(request.user, 'hrprofile'):
        applied_job_ids = Application.objects.filter(applicant=request.user).values_list('job_id', flat=True)
        
    categories = Category.objects.all()
    
    try:
        selected_category_id = int(category_id) if category_id else None
    except ValueError:
        selected_category_id = None

    return render(request, 'job_list.html', {'jobs': jobs, 'applied_job_ids': applied_job_ids, 'query': query, 'categories': categories, 'selected_category': selected_category_id})

from django.contrib import messages

@login_required
def apply_job(request, job_id):
    job = Job.objects.get(id=job_id)
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
    else:
        Application.objects.create(job=job, applicant=request.user)
        messages.success(request, 'Successfully applied for the job!')
    return redirect('job_list')

@login_required
@hr_required
def employer_dashboard(request):
    jobs = Job.objects.filter(posted_by=request.user)
    return render(request, 'employer_dashboard.html', {'jobs': jobs})

from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Application, ApplicationMessage

def manage_application(request, application_id):
    application = get_object_or_404(Application, id=application_id)
    
    # Security check: User must be applicant or job poster
    if request.user != application.applicant and request.user != application.job.posted_by:
        return redirect('home')

    if request.method == 'POST':
        # Handle Message
        if 'message_content' in request.POST:
            # Restriction: Applicant cannot start conversation
            if request.user == application.applicant and not application.messages.exists():
                messages.error(request, "You cannot send a message until the recruiter contacts you.")
                return redirect('manage_application', application_id=application_id)

            content = request.POST.get('message_content')
            if content:
                ApplicationMessage.objects.create(
                    application=application,
                    sender=request.user,
                    content=content
                )
                messages.success(request, 'Message sent successfully.')
                return redirect('manage_application', application_id=application_id)

        # Handle Status Update (Only for Job Poster)
        if 'status' in request.POST and request.user == application.job.posted_by:
            new_status = request.POST.get('status')
            application.status = new_status
            application.save()
            messages.success(request, f'Application status updated to {new_status}.')
            return redirect('manage_application', application_id=application_id)

    # Get conversation history
    conversation = application.messages.all()
    
    return render(request, 'application_detail.html', {
        'application': application,
        'conversation': conversation,
        'is_recruiter': request.user == application.job.posted_by
    })