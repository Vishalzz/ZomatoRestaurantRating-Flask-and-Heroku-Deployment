import flask
from flask import Flask,request,render_template
from flask_cors import cross_origin
import sklearn
import pickle
import pandas as pd

import numpy as np

app = Flask(__name__)

@app.route('/')
@cross_origin()
def hello():
	return render_template("index.html")

pickle_in = open('model.pkl','rb')
model = pickle.load(pickle_in)



@app.route("/predict", methods=["GET", "POST"])
@cross_origin()

def predict():
	if request.method == "POST":

		column_train = ['location_Banashankari', 'location_Bannerghatta Road',
				'location_Bellandur', 'location_Brigade Road',
				'location_Electronic City', 'location_HSR', 'location_Indiranagar',
				'location_JP Nagar', 'location_Jayanagar',
				'location_Koramangala 1st Block', 'location_Koramangala 4th Block',
				'location_Koramangala 5th Block', 'location_Koramangala 6th Block',
				'location_Koramangala 7th Block', 'location_MG Road',
				'location_Marathahalli', 'location_Sarjapur Road', 'location_Ulsoor',
				'location_Whitefield', 'location_other_location', 'rest_type_Bar',
				'rest_type_Beverage Shop', 'rest_type_Cafe', 'rest_type_Casual Dining',
				'rest_type_Casual Dining, Bar', 'rest_type_Delivery',
				'rest_type_Dessert Parlor', 'rest_type_Quick Bites',
				'rest_type_Takeaway, Delivery', 'rest_type_other_rest_type',
				'cuisines_Bakery, Desserts', 'cuisines_Biryani', 'cuisines_Cafe',
				'cuisines_Chinese', 'cuisines_Chinese, North Indian',
				'cuisines_Desserts', 'cuisines_Fast Food',
				'cuisines_Ice Cream, Desserts', 'cuisines_Mithai, Street Food',
				'cuisines_North Indian', 'cuisines_North Indian, Chinese',
				'cuisines_North Indian, Chinese, Biryani', 'cuisines_South Indian',
				'cuisines_South Indian, North Indian, Chinese',
				'cuisines_other_cuisines', 'type_Cafes', 'type_Delivery',
				'type_Desserts', 'type_Dine-out', 'type_Drinks & nightlife',
				'type_Pubs and bars', 'online_order', 'book_table', 'votes', 'cost',
				'reviews_list']

		#Location
		Location = request.form["Location"]
		locations_train_column = column_train[:20]
		locations_input =[0]*20
		locations_column = []
		for location in locations_train_column:


			new_location = location.replace("location_","")
			locations_column.append(new_location)

		for i in range(20):

			if locations_column[i]==Location:

				locations_input[i] =1

		#Rest_type
		Rest_type = request.form["Rest_type"]
		rest_type_train_column = column_train[20:30]
		rest_type_input =[0]*10
		rest_type_column = []
		for rest_type in rest_type_train_column:

			new_rest_type = rest_type.replace("rest_type_","")
			rest_type_column.append(new_rest_type)
		for i in range(10):

			if rest_type_column[i]==Rest_type:

				rest_type_input[i] =1

		# cuisines
		Cuisines = request.form["Cuisines"]
		cuisines_train_column = column_train[30:45]
		cuisines_input =[0]*15
		cuisines_column = []
		for cuisines in cuisines_train_column:

			new_cuisines = cuisines.replace("cuisines_","")
			cuisines_column.append(new_cuisines)
		for i in range(15):
			if cuisines_column[i]==Cuisines:
				cuisines_input[i]=1

		## Service _type
		Service_type = request.form["Service_type"]
		service_type_train_column = column_train[45:51]
		service_type_input =[0]*6
		service_type_column = []
		for service_type in service_type_train_column:
			new_service_type = service_type.replace("type_","")
			service_type_column.append(new_service_type)
		for i in range(6):
			if service_type_column[i]==Service_type:
				service_type_input[i]=1

		#online_order
		Online_order = request.form["Online_order"]
		online_order_input = []
		if Online_order=='Yes':

			new_online_order = 1
			online_order_input.append(new_online_order)
		else:

			new_online_order = 0
			online_order_input.append(new_online_order)

		# book_table
		Book_table = request.form["Book_table"]
		book_table_input = []
		if Book_table=='Yes':
			new_book_table = 1
			book_table_input.append(new_book_table)
		else:
			new_book_table = 0
			book_table_input.append(new_book_table)

		# votes
		votes_input = [np.log(int(request.form["Votes"]))]
		# Cost
		cost_input = [np.log(float(request.form["Cost"]))]
		# reviews_list
		review_list_input = [request.form["Reviews_list"]]




		input = locations_input + rest_type_input + cuisines_input + service_type_input + online_order_input + book_table_input + votes_input + cost_input + review_list_input  
		prediction=model.predict([input])


		output = round(prediction[0], 2)

		return render_template('index.html', prediction_text="Restaurant rating is {}".format(output))

	return render_template("index.html")


if __name__ == "__main__":

	app.run(debug=True)







