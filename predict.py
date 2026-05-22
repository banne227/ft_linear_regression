

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
		f.write("0.0 0.0")
		f.close()
		return "0.0 0.0"



def predict(mileage):
	thetas = [float(x) for x in get_thetas().split()]
	return thetas[0] + (thetas[1] * mileage)


if __name__ == "__main__":
	try:
		mileage = float(get_km())
	except ValueError:
		print("Veuillez entrer un nombre valide pour le kilometrage.")
		exit(1)
	if mileage < 0:
		print("Veuillez entrer un nombre valide pour le kilometrage.")
	else:
		print(predict(mileage))