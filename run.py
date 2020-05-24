from flaskapp import app

if __name__ == '__main__':
	print("\n*******************App started*****************\n")
	# run overall
	#app.run(debug=True,  host='0.0.0.0')
	# run in localhost
	app.run(debug=True)
