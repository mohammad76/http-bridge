import json

import requests
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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


@csrf_exempt
def send_mail_view(request):
    if request.method == 'POST':
        data = json.loads(request.body.decode('utf-8'))
        subject = data.get('subject', '')
        a_from = data.get('from', '')
        to = data.get('to', '')
        body = data.get('body', '')
        SMTP_SERVER = data.get('smtp_server', '')
        SMTP_PORT = data.get('smtp_port', '')
        USERNAME = data.get('username', '')
        PASSWORD = data.get('password', '')
        USE_TLS = True  # اگر روی 465 زدی کنش False و پورت رو بزار 465

        if not subject or not to or not body:
            return JsonResponse({'error': 'Missing subject, to, or body parameter'}, status=400)

        msg = MIMEMultipart("alternative")
        msg['Subject'] = 'تست SMTP از Python'
        msg['From'] = a_from
        msg['To'] = to

        html_content = body
        mime_text = MIMEText(html_content, "html")
        msg.attach(mime_text)
        try:
            if USE_TLS:
                server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT, timeout=10)
                server.ehlo()
                server.starttls()
                server.login(USERNAME, PASSWORD)
            else:
                server = smtplib.SMTP_SSL(SMTP_SERVER, SMTP_PORT, timeout=10)
                server.login(USERNAME, PASSWORD)

            server.sendmail(a_from, [to], msg.as_string())
            server.quit()
            return JsonResponse({'msg': 'ok'}, status=200)
        except Exception as e:
            return JsonResponse({'error': 'prm in send'}, status=500)
    return JsonResponse({'error': 'Only POST supported'}, status=405)
