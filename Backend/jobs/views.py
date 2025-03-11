from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import logging
from django.conf import settings

logger = logging.getLogger(__name__)

##///TODO: 1. take i/p from html form - job (description)  
##///TODO: 2. resume/cv i/p 
##TODO: 3. convert both into json n send to groq 
##TODO: 4. recieve the percentage of probability of getting interview call 
##TODO: 5. send data to frontend html n show result to user 
class JobCompareView(APIView):
    def get(self, request):
        return render(request, "jobs/landing_page.html")

    def post(self, request):
        """Handle resume and job description submission"""

        # Get job description from form
        job_description = request.POST.get("job_description")

        # Get resume file from form
        resume_file = request.FILES.get("resume")

        if not job_description or not resume_file:
            return Response({"error": "Missing job description or resume"}, status=400)

        # ✅ Save the uploaded resume file in the 'media/resumes/' folder
        file_path = f"resumes/{resume_file.name}"
        saved_path = default_storage.save(file_path, ContentFile(resume_file.read()))

        # Get the absolute file path
        full_file_path = os.path.join(settings.MEDIA_ROOT, saved_path)

        print(f"Received Resume: {resume_file.name}")
        print(f"Saved at: {full_file_path}")  # ✅ This will confirm the file is being saved
        logger.debug(f"File saved at: {full_file_path}")

        return Response({
            "message": "Data received!",
            "job_description": job_description,
            "resume_filename": resume_file.name,
            "file_path": full_file_path
        })
