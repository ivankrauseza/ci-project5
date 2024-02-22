from .models import Basket  # Replace 'your_app' with the actual name of your app


def basket_item_count(request):
    user = request.user
    count = 0
    if user.is_authenticated:
        count = Basket.objects.filter(user=user, transaction="B").count()
    return {'basket_item_count': count}
