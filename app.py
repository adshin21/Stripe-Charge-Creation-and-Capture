from flask import Flask, request, jsonify
from config import stripe_api_key
import stripe
stripe.api_key = stripe_api_key
app = Flask(__name__)



@app.route("/api/v1/get_charges", methods=["GET",])
def get_charges():
    """
    :return: List of charge object
    """
    charge_list = stripe.Charge.list(captured=False)

    return { "data": {
        "charges": charge_list
    }}, 200



@app.route("/api/v1/create_charge", methods=["POST", "OPTIONS"])
def create_charge():
    """
    :param:
        amount :-> int ( required )
        currency :-> str ( default => USD )
        card_details :-> dict (
                            "object": "card" ( required ),
                            "number": str ( required ),
                            "exp_month": int ( required ),
                            "exp_year": int (year) ( required ),
                            "cvc": str ( required )
                        ) => required

        name :-> str
        address :-> dict (
                        keys:
                            "line1": str ( required ),
                            "city": str ( required )",
                            "state": state code, str ( required ),
                            "country": country code, str ( required ),
                            "postal_code": str ( required )
                        )
        customer_id :-> str ( stripe customer id if present )

    :return:
        customer_id :-> Str
        charge :-> Charge Object
        charge_id :-> Str
        time_of_charge_creation :-> Time Stamp
        captured :-> bool
    """


    request_data = request.get_json(force=True)
    amount = request_data.get("amount", 0)
    currency = request_data.get("currency", "usd")
    name = request_data.get("name", "")
    address = request_data.get("address", {})
    card_details = request_data.get("card", {})
    customer_id = request_data.get("customer_id", None)

    customer = None
    if customer_id:
        try:
            customer = stripe.Customer.retrieve(customer_id)
        except stripe.error.InvalidRequestError:
            # customer is not present we'll create new customer for now
            pass

    token = stripe.Token.create(
        card=card_details
    )

    if not customer:
        customer = stripe.Customer.create(
            name=name,
            address=address,
            source=token
        )

    charge = stripe.Charge.create(
        amount=amount,
        currency=currency,
        description="Ok so charge is created",
        capture=False,
        customer=customer
    )

    return { "data": {
        "customer_id": charge["customer"],
        "charge_id": charge["id"],
        "captured": charge["captured"],
        "created": charge["created"],
        "charge": charge
    } }, 200



@app.route("/api/v1/capture_charge/<charge_id>", methods=["GET",])
def capture_charge(charge_id):
    """
    :param charge_id: str ( required )
    :return: captured charge object
    """
    captured_charge = None
    try:
        captured_charge = stripe.Charge.capture(charge_id)
    except stripe.error.InvalidRequestError as e:
        # either charge is already captured or bad charge id
        return { "data": {
            "msg": str(e),
            "charge_id": charge_id
        }}, 400

    return { "data": {
        "charge_id": charge_id,
        "captured_charge": captured_charge
    }}, 200


@app.route("/api/v1/create_refund/<charge_id>", methods=["GET",])
def refund_charge(charge_id):
    """
    :param charge_id:
    :return: refunded object
    """
    refunded_charge = None
    try:
        refunded_charge = stripe.Refund.create(charge=charge_id)
    except stripe.error.InvalidRequestError as e:
        return { "data": {
            "msg": str(e),
            "charge_id": charge_id
        }}, 400

    return { "data": {
        "charge_id": charge_id,
        "refunded_charge": refunded_charge
    }}

if __name__ == "__main__":
    app.run()
