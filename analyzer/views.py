from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils.decorators import method_decorator
import json
from .models import PlagiarismReport
from .utils import analyze_plagiarism, extract_text_from_file, validate_file
import nltk
nltk.download('punkt', quiet=True)
nltk.download('punkt_tab', quiet=True)



def landing_page(request):
    """
    Landing page - redirects to dashboard if authenticated
    """
    if request.user.is_authenticated:
        return redirect('analyzer:dashboard')
    return render(request, 'landing.html')


class DashboardView(LoginRequiredMixin, TemplateView):
    """
    Main dashboard for plagiarism analysis
    """
    template_name = 'analyzer/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get user's recent reports
        context['reports'] = PlagiarismReport.objects.filter(
            user=self.request.user
        )[:10]  # Last 10 reports
        return context


@csrf_exempt
@require_http_methods(["POST"])
@login_required
def analyze_api(request):
    """
    API endpoint for plagiarism analysis
    """
    try:
        # Get text from request
        text_input = request.POST.get('text', '').strip()
        uploaded_file = request.FILES.get('file')
        
        # Validate input
        if not text_input and not uploaded_file:
            return JsonResponse({
                'error': 'Please provide either text input or upload a file'
            }, status=400)
        
        # Extract text from file if provided
        if uploaded_file:
            try:
                validate_file(uploaded_file)
                text_input = extract_text_from_file(uploaded_file)
            except ValueError as e:
                return JsonResponse({'error': str(e)}, status=400)
        
        # Validate text length
        if len(text_input.strip()) < 50:
            return JsonResponse({
                'error': 'Text must be at least 50 characters long'
            }, status=400)
        
        # Perform plagiarism analysis
        analysis_result = analyze_plagiarism(text_input)
        
        # Save report to database
        report = PlagiarismReport.objects.create(
            user=request.user,
            original_text=text_input,
            file=uploaded_file if uploaded_file else None,
            similarity_score=analysis_result['similarity_score'],
            flagged_sentences=analysis_result['flagged_sentences']
        )
        
        # Return analysis results
        return JsonResponse({
            'success': True,
            'report_id': report.id,
            'similarity_score': analysis_result['similarity_score'],
            'flagged_sentences': analysis_result['flagged_sentences'],
            'total_sentences': analysis_result['total_sentences'],
            'flagged_count': analysis_result['flagged_count'],
            'risk_level': report.risk_level,
            'created_at': report.created_at.strftime('%Y-%m-%d %H:%M:%S')
        })
        
    except Exception as e:
        return JsonResponse({
            'error': f'An error occurred during analysis: {str(e)}'
        }, status=500)


@login_required
def report_detail(request, report_id):
    """
    View detailed report
    """
    try:
        report = PlagiarismReport.objects.get(id=report_id, user=request.user)
        return render(request, 'analyzer/report_detail.html', {'report': report})
    except PlagiarismReport.DoesNotExist:
        return redirect('dashboard')
