from django.shortcuts import render
from .models import *
from .seralizer import taraz_ser
from rest_framework import generics
from django.http import HttpResponse
import json

from django.http import JsonResponse
from .models import taraz
import openai

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from .models import taraz
import openai

# Установите свой API-ключ от OpenAI здесь
openai.api_key = "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"

def home_page(request):
    if request.method == 'POST':
        danni = request.POST.get('name_sea')  # Получение данных из поля 'name_sea' в форме
        
        if danni:
            # Извлечение данных из модели taraz
            danni2 = taraz.objects.all().values_list('name_sea', 'size_sez')
            danni_str = ", ".join([f"{name} ({size}km)" for name, size in danni2])
            
            # Формирование prompt
            prompt_data = f"Вопрос: {danni}\nДанные озер: {danni_str}"
            
            # Отправка запроса к модели GPT-3
            response = openai.Completion.create(
                engine="text-davinci-002",
                prompt=prompt_data,
                max_tokens=100
            )
            
            # Получение сгенерированного текста из ответа
            response_text = response.choices[0].text.strip()
            
            return JsonResponse({"message": response_text})
        else:
            return JsonResponse({"message": "Пустой запрос"})
    else:
        # Обработка GET-запроса
        context = taraz.objects.all() 
        return render(request, 'home.html', {'ozender': context})


class tarazListView(generics.ListCreateAPIView):
    queryset = taraz.objects.all()
    serializer_class = taraz_ser

