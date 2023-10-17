from django.shortcuts import redirect, get_object_or_404
from monitoring.models import UserStock

def delete_user_stock(request, user_stock_id):
    user_stock = get_object_or_404(UserStock, pk=user_stock_id)
    if request.method == 'POST':
        user_stock.delete()

    return redirect('home')