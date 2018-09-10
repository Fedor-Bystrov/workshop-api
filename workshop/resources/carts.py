import ujson

from falcon import Request, Response, status_codes, HTTPBadRequest

from workshop.model import Cart
from workshop.repository import Repository


class CartListResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_get(self, request: Request, response: Response) -> None:
        carts = self._repository.get_all(self._type)
        cart_list = list()
        for cart in carts:
            cart_list.append({
                'cartId': cart.cart_id,
                'creationTime': cart.creation_time.isoformat(),
                'customerId': cart.customer_id,
                'price': str(cart.price),
                'description': cart.description,
                'shippingAddress': cart.shipping_address,
            })

        response.body = ujson.dumps(cart_list)
        response.status = status_codes.HTTP_OK


class CartResource:

    def __init__(self, repository: Repository) -> None:
        self._repository = repository
        self._type = Cart

    def on_get(self, request: Request, response: Response, cart_id: int) -> None:
        try:
            cart = self._repository.get(self._type, cart_id)
            if not cart:
                # TODO тут кидать более специфичный exception
                raise RuntimeError('Cart with id = {} not found!'.format(cart_id))

            response.body = ujson.dumps({
                'cartId': cart.cart_id,
                'creationTime': cart.creation_time.isoformat(),
                'customer': {
                    'customerId': cart.customer_id,
                    'creationTime': cart.customer.creation_time.isoformat(),
                    'firstName': cart.customer.first_name,
                    'lastName': cart.customer.last_name,
                    'middleName': cart.customer.middle_name,
                    'locale': cart.customer.locale.value,
                    'email': cart.customer.email,
                    'phone': cart.customer.phone,
                },
                'price': str(cart.price),
                'purchases': [{'productId': p.product_id, 'quantity': p.quantity} for p in cart.purchases],
                'description': cart.description,
                'shippingAddress': cart.shipping_address,
            })
            response.status = status_codes.HTTP_OK

        except RuntimeError:
            raise HTTPBadRequest()
