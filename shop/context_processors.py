from .models import Transaction  # Replace 'your_app' with the actual name of your app


def basket_item_count(request):
    user = request.user
    count = 0
    if user.is_authenticated:
        count = Transaction.objects.filter(user=user, type="B").count()
    return {'basket_item_count': count}
