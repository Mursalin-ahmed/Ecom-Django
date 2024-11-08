from Product.models import Category

def category(request):
    cat = Category.objects.all()[::-1]
    return {'cat': cat}
