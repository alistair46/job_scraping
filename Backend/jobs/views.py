import os
from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import json
import re #Regex 
import requests
import pdfplumber
import docx
from groq import Groq


##///TODO: 1. take i/p from html form - job (description)  
##///TODO: 2. resume/cv i/p 
#///#TODO: 3. convert both into json n send to groq 
#///#TODO: 4. recieve the percentage of probability of getting interview call 
##TODO: 5. send data to frontend html n show result to user 
    
class JobCompareView(APIView):
    def get(self, request):
        return render(request, "jobs/landing_page.html")

    def post(self, request):
        # Extract: Get job description and resume file
        job_description = request.POST.get("job_description")
        resume_file = request.FILES.get("resume")

        if not job_description or not resume_file:
            return Response({"error": "Missing job description or resume"}, status=400)

        # Save the uploaded file
        file_path = f"resumes/{resume_file.name}"
        saved_path = default_storage.save(file_path, ContentFile(resume_file.read()))

        # Extract text from the resume
        resume_text = self.extract_text_from_resume(resume_file)

        # Convert to JSON
        data = {
            "job_description": job_description,
            "resume_text": resume_text,  # Send extracted text
            "resume_filename": resume_file.name
        }

        json_data = json.dumps(data)  # Convert to JSON format

        # Send to Groq API
        api_key =os.environ.get('GROQ_API')  # Use an environment variable instead of hardcoding
        client = Groq(api_key=api_key) 
        try:
            chat_completion = client.chat.completions.create(
            model="llama3-70b-8192",  # Ensure this model exists in Groq's API
            messages=[
                {"role": "system", "content": "You are an IT company ATS system. Based on the submitted CV and job description, you will only output a percentage rating indicating how compatible the CV is with the job. No other details, just a percentage."},
                {"role": "user", "content": f"Job Description:\n{data['job_description']}\n\nCV:\n{data['resume_text']}"}
            ],
            temperature=0,  # Deterministic output
            max_tokens=50,  # Limit response size
            top_p=1,
            stream=False,
)

# Print the compatibility score
            print(chat_completion.choices[0].message.content)
            groq_response = json.dumps(chat_completion.to_dict())
        except requests.exceptions.RequestException as e:
            return Response({"error": f"Failed to send data to Groq API: {str(e)}"}, status=500)

        return Response({
            "message": "Data sent successfully!",
            "data_sent": data,
            "groq_response": groq_response
        })

    def extract_text_from_resume(self, resume_file):
        """Extract text from a PDF or DOCX resume"""
        if resume_file.name.endswith(".pdf"):
            return self.extract_text_from_pdf(resume_file)
        elif resume_file.name.endswith(".docx"):
            return self.extract_text_from_docx(resume_file)
        else:
            return "Unsupported file format"

    def extract_text_from_pdf(self, pdf_file):
        """Extract text from a PDF resume"""
        text = ""
        try:
            with pdfplumber.open(pdf_file) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() + "\n"
        except Exception as e:
            return f"Error extracting PDF: {str(e)}"
        return text.strip(), print(text)

    def extract_text_from_docx(self, docx_file):
        """Extract text from a DOCX resume"""
        try:
            doc = docx.Document(docx_file)
            
            return "\n".join([para.text for para in doc.paragraphs]).strip()
        except Exception as e:
            return f"Error extracting DOCX: {str(e)}",print(doc)

