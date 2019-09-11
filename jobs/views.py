from django.shortcuts import render
from .models import Job
from faker import Faker
from decouple import config
import requests


# Create your views here.

def index(request):
    return render(request, 'jobs/index.html')

def pastlife(request):
    name = request.POST.get('name')
    if not Job.objects.filter(name=name):
        fake = Faker('ko_KR')
        job = Job()
        job.name = name
        job.my_job = fake.job()
        job.save()
    else:
        job = Job.objects.filter(name=name)[0]
    # 1. 직업 결과에 따라 요청
    api_key = config('GIPHY_API_KEY')
    # 2. url 설정
    url = f'http://api.giphy.com/v1/gifs/search?api_key={api_key}&q={job.my_job}&lang=ko'
    # 3. pip requests설치, import
    response = requests.get(url).json()
    # 4. 응답 결과에서 이미지 url뽑기
    try:
        image_url = response['data'][0].get('images').get('original').get('url')
    except:
        image_url = None
    context = {
        'job': job,
        'image_url': image_url
    }    
    return render(request, 'jobs/pastlife.html', context)
