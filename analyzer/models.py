from django.db import models
from django.conf import settings
import json


class PlagiarismReport(models.Model):
    """
    Model to store plagiarism analysis reports
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='reports')
    original_text = models.TextField()
    file = models.FileField(upload_to='uploads/', blank=True, null=True)
    similarity_score = models.FloatField(help_text="Similarity score as percentage (0-100)")
    flagged_sentences = models.JSONField(default=list, help_text="List of flagged sentences with sources")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Report by {self.user.username} - {self.similarity_score}% similarity"
    
    @property
    def flagged_sentences_count(self):
        """Return the number of flagged sentences"""
        return len(self.flagged_sentences) if self.flagged_sentences else 0
    
    @property
    def risk_level(self):
        """Return risk level based on similarity score"""
        if self.similarity_score >= 70:
            return "High"
        elif self.similarity_score >= 40:
            return "Medium"
        else:
            return "Low"
