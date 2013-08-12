'''
	A simple Flask app for making Stripe payments
	Author: Muneeb Ali | http://muneeb.org
	Modified from examples at http://stripe.com/docs/
	License: MIT (see LICENSE)  
'''

from flask import Flask, render_template, request
import stripe

from config import stripe_keys 
from config import DEFAULT_CHARGE_AMOUNT, DEFAULT_CHARGE_DESCRIPTION
from config import DB_NAME 

stripe.api_key = stripe_keys['secret_key']

app = Flask(__name__)

#-----------------------------------
# MongoDB for stripe customers
from pymongo import MongoClient
c = MongoClient()
db = c[DB_NAME]
posts = db.posts

#-----------------------------------
@app.route('/')
def index():
	return render_template('index.html', 
					key=stripe_keys['publishable_key'],
					amount_usd=get_amount_usd()
					)

#-----------------------------------
def get_amount_usd(amount=DEFAULT_CHARGE_AMOUNT):
		return float(amount) / 100

#-----------------------------------
def get_stripe_customer(customer_email):

	customer_info = posts.find_one({"customer_email":customer_email})

	if(customer_info == None):
		return False, customer_info
	else:
		return True, customer_info

#-----------------------------------
def save_stripe_customer(customer_email, customer_id):

	# If already have a customer by that email, delete old entry
	reply, entry = get_stripe_customer(customer_email)
	if(reply):
		posts.remove(entry)
	else:
		post = {"customer_email":customer_email,"customer_id":customer_id}
		posts.insert(post)

#-----------------------------------
def stripe_charge(customer_id,
			charge_amount=DEFAULT_CHARGE_AMOUNT,
			charge_descripton=DEFAULT_CHARGE_DESCRIPTION):

	try:		
		charge = stripe.Charge.create(
			customer=customer_id,
			amount=charge_amount,
			currency='usd',
			description=charge_descripton 
			)

	except stripe.CardError as e:
		
		# The card has been declined (or other error)
		return False, e 

	return True, "successfully charged"
	
#-----------------------------------
@app.route('/charge', methods=['POST'])
def charge():

	customer_email = request.form['email']

	# Check if already have this customer
	customer_valid, customer_info = get_stripe_customer(customer_email)

	if(customer_valid):
		customer_id = customer_info['customer_id']
	else:

		customer = stripe.Customer.create(
					email=customer_email,
					card=request.form['stripeToken']
					)

		customer_id = customer.id

		# save the customer ID in DB for later use
		save_stripe_customer(customer_email, customer_id)

	# charge the customer (new or already present in DB)
	charge_valid, charge_msg = stripe_charge(customer_id)

	return render_template('charge.html', 
					amount_usd=get_amount_usd(), 
					customer_email=customer_email,
					charge_valid=charge_valid,
					charge_msg=charge_msg)

#-----------------------------------
@app.route('/recurring', methods=['POST'])
def recurring():

	customer_email = request.form['email']

	# Get customer_id from Mongo
	customer_valid, customer_info = get_stripe_customer(customer_email)

	if(customer_valid):
		customer_id = customer_info['customer_id']
		
		# Charge the customer (new or already present in DB)
		charge_valid, charge_msg = stripe_charge(customer_id)

	else:
		charge_valid = False
		charge_msg = "recurring customer doesn't exist"

	return render_template('charge.html', 
					amount_usd=get_amount_usd(), 
					customer_email=customer_email,
					charge_valid=charge_valid,
					charge_msg=charge_msg)

#-----------------------
if __name__ == '__main__':

	app.run(debug=True)