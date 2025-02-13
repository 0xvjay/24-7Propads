import json
import logging

import stripe
from django.conf import settings


class StripeSubscriptionHandler:
    def __init__(self, api_key):
        self.stripe = stripe.api_key = api_key
        self.logger = logging.getLogger("app")

    def create_plan(self, name, description, price, interval="month"):
        try:
            stripe_product = stripe.Product.create(
                name=name,
                description=description,
            )
            stripe_price = stripe.Price.create(
                unit_amount=int(price * 100),
                currency="inr",
                recurring={"interval": interval},
                product=stripe_product.id,
                nickname=name,
            )
            self.logger.info(
                f"Successfully created plan: {stripe_product.id}-{stripe_price.id}"
            )
            return (stripe_product.id, stripe_price.id)
        except Exception as e:
            self.logger.exception(f"Error creating plan: {str(e)}")
            return None

    def delete_plan(self, product_id, price_id):
        try:
            stripe.Product.modify(product_id, active=False)
            stripe.Product.modify(price_id, active=False)
            return True
        except Exception as e:
            self.logger.exception(f"Error deleting plan: {str(e)}")
            return False

    def create_checkout_session(self, price_id, user):
        success_url = settings.SITE_URL + "subscriptions/success/"
        cancel_url = settings.SITE_URL + "subscriptions/cancel/"
        try:
            session = stripe.checkout.Session.create(
                success_url=success_url,
                cancel_url=cancel_url,
                line_items=[{"price": price_id, "quantity": 1}],
                mode="subscription",
                customer_email=user.email,
            )
            self.logger.info(f"Successfully created checkout session: {session.id}")
            return session.id
        except Exception as e:
            self.logger.exception(f"Error creating checkout session: {str(e)}")
            return None

    def update_plan(
        self, product_id, price_id, name, description, price, interval="month"
    ):
        try:
            # set current to inactive
            stripe.Price.modify(price_id, active=False)

            # create new
            stripe_price = stripe.Price.create(
                unit_amount=int(price * 100),
                currency="inr",
                recurring={"interval": interval},
                product=product_id,
                nickname=name,
            )
            stripe.Product.modify(
                product_id,
                name=name,
                description=description,
                default_price=stripe_price.id,
            )
            self.logger.info(
                f"Successfully updated plan: {product_id}-{stripe_price.id}"
            )
            return product_id, stripe_price.id
        except Exception as e:
            self.logger.exception(f"Error updating plan: {str(e)}")

    def create_event(self, data):
        try:
            payload = json.loads(data)
            return stripe.Event.construct_from(payload, stripe.api_key)
        except Exception as e:
            self.logger.exception(f"Error creating event: {str(e)}")
            return None

    def retrieve_subscription_plan(self, plan_id):
        try:
            return stripe.Subscription.retrieve(plan_id)
        except Exception as e:
            self.logger.exception(f"Error retrieving customer: {str(e)}")
            return None
