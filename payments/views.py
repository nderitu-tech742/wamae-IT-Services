from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
import json

_payments = []

@csrf_exempt
def add_payment(request):
    if request.method == 'POST':
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body.decode('utf-8'))
            else:
                data = request.POST

            name = data.get('name')
            amount = data.get('amount')

            if not name or not amount:
                return JsonResponse({'error': 'Both name and amount are required.'}, status=400)

            try:
                amount = float(amount)
            except ValueError:
                return JsonResponse({'error': 'Amount must be a number.'}, status=400)

            entry = {'name': name, 'amount': amount}
            _payments.append(entry)
            return JsonResponse({'status': 'success', 'payment': entry})

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON format.'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)

    return render(request, 'payments/add_payment.html')


def list_payments(request):
    return JsonResponse({'payments': _payments}, safe=False)
