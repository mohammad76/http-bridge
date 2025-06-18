import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def proxy_view(request):
    if request.method == 'POST':
        try:
            # ورودی را بخوان
            body = json.loads(request.body)
            method = body.get('method', 'GET').upper()
            url = body['url']
            data = body.get('data')
            headers = body.get('headers', {})

            # ارسال ریکویست به مقصد
            resp = requests.request(
                method=method,
                url=url,
                headers=headers,
                data=data,
                timeout=20
            )

            # تبدیل نوع پاسخ
            content_type = resp.headers.get('Content-Type', 'application/json')
            return HttpResponse(resp.content, status=resp.status_code, content_type=content_type)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    return JsonResponse({'error': 'Only POST supported'}, status=405)
