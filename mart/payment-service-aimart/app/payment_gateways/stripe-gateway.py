from app.payment_settings import stripe_API_Key


# Stripe API keys
stripe.api_key = stripe_API_Key

def create_payment_session(amount, currency="USD", description="Payment Description"):
    try:
        session = stripe.checkout.Session.create(
            payment_method_types=['card'],
            line_items=[{
                'price_data': {
                    'currency': currency,
                    'product_data': {
                        'name': 'Payment',
                    },
                    'unit_amount': int(amount * 100),  # Amount in cents
                },
                'quantity': 1,
            }],
            mode='payment',
            success_url='http://localhost:8000/success',
            cancel_url='http://localhost:8000/cancel',
            metadata={
                'description': description,
            }
        )
        return session.url
    except stripe.error.StripeError as e:
        print(f"Stripe Error: {e}")
        return None

if __name__ == "__main__":
    # Example usage:
    amount = 100.0  # Amount in dollars
    payment_url = create_payment_session(amount)
    print(f"Payment URL: {payment_url}")
