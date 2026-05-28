

def get_km():
	valeur = input("Votre kilometrage: ")
	return valeur

def get_thetas():
	try:
		with open("thetas.txt", "r") as f:
			contenu = f.read()
			return contenu

	except FileNotFoundError:
		f = open("thetas.txt", "x")
		f.write("0.0 0.0 0.0 0.0 0.0 0.0")
		f.close()
		return "0.0 0.0"



def predict(mileage):
	thetas = [float(x) for x in get_thetas().split()]

	if len(thetas) != 6:
		raise ValueError("Le fichier thetas.txt doit contenir exactement 6 valeurs: theta0, theta1, mini_mile, maxi_mile, min_price, maxi_price.")
	theta0, theta1, mini_mile, maxi_mile , min_price, maxi_price = thetas
	if maxi_mile == mini_mile:
		normalized_prediction = theta0
	else:
		normalized_mileage = (mileage - mini_mile) / (maxi_mile - mini_mile)
		normalized_prediction = theta0 + (theta1 * normalized_mileage)
	return normalized_prediction * (maxi_price - min_price) + min_price


if __name__ == "__main__":
	try:
		mileage = float(get_km())
	except ValueError:
		print("Veuillez entrer un nombre valide pour le kilometrage.")
		exit(1)
	if mileage < 0:
		print("Veuillez entrer un nombre valide pour le kilometrage.")
	else:
		try:
			print(predict(mileage))
		except ValueError as e:
			print(e)