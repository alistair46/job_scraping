from django.shortcuts import render
from rest_framework.views import APIView
import json


#TODO: 1. take i/p from html form - job (description) 
#TODO: 2. resume/cv i/p 
#TODO: 3. convert both into json n send to groq 
#TODO: 4. recieve the percentage of probability of getting interview call 
#TODO: 5. send data to frontend html n show result to user 
class job_compare_2_cv(APIView):
    def extract(request):
        if request.POST:
            variable1=1

    pass