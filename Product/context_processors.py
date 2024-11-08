# myapp/context_processors.py
from .models import Product

def product_id(request):
    # Default to None if there's no product in the context
    product_id = None

    # Check if the product ID is in the URL or session (or retrieve in another way)
    # This example assumes you've stored the product ID in the session previously
    if 'product_id' in request.session:
        try:
            product_id = request.session['product_id']
        except Product.DoesNotExist:
            pass

    # Return a dictionary to add this data to the template context
    return {'product_id': product_id}
