import math
import matplotlib.pyplot as plt

learning_rate = 0.5
iterations = 2000

def get_thetas():
	try:
		with open("thetas.txt", "r") as f:
			contenu = f.read()
			return contenu

	except FileNotFoundError:
		f = open("thetas.txt", "x")
		f.write("0.0 0.0 0.0 0.0 0.0 0.0")
		f.close()
		return "0.0 0.0 0.0 0.0 0.0 0.0"

def estimate_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)

def show_data(mileage, prices, theta0=None, theta1=None, mini_mile=None):
	plt.scatter(mileage, prices, label="Données réelles")
	if theta0 is not None and theta1 is not None and mini_mile is not None:
		x_line = [min(mileage), max(mileage)]
		y_line = [theta0 + theta1 * (x - mini_mile) for x in x_line]
		plt.plot(x_line, y_line, 'r-', label="Droite de régression")
		plt.legend()
	plt.xlabel("Kilometrage")
	plt.ylabel("Prix")
	plt.title("Prix en fonction du kilometrage")
	plt.show()

def train(file):
	mileage = []
	prices = []

	with open(file, "r") as f:
		for	line in f:
			if line == "km,price\n":
				continue
			data = line.split(",") 
			mileage.append(float(data[0]))
			prices.append(float(data[1]))

	mileage_orig = mileage[:]
	prices_orig = prices[:]
	mini_mile = min(mileage)
	maxi_mile = max(mileage)
	if maxi_mile == mini_mile:
		raise ValueError("Les kilometrages sont tous identiques, impossible de normaliser.")

	min_price = min(prices)
	maxi_price = max(prices)
	if maxi_price == min_price:
		raise ValueError("Les prix sont tous identiques, impossible de normaliser.")


	for i in range(len(mileage)):
		mileage[i] = (mileage[i] - mini_mile) / (maxi_mile - mini_mile)
		prices[i] = (prices[i] - min_price) / (maxi_price - min_price)

	theta0 = 0.0
	theta1 = 0.0

	m = len(mileage)

	for _ in range(iterations):
		sum_error = 0
		sum_error_mileage = 0
		for i in range(len(mileage)):
			price_estimate = estimate_price(mileage[i], theta0, theta1)
			error = price_estimate - prices[i]
			sum_error += error
			sum_error_mileage += error * mileage[i]

		tmp_t0 = learning_rate * (1 / m) * sum_error
		tmp_t1 = learning_rate * (1 / m) * sum_error_mileage

		theta0 = theta0 - tmp_t0
		theta1 = theta1 - tmp_t1
		if not math.isfinite(theta0) or not math.isfinite(theta1):
			print("Erreur: overflow numerique pendant l'entrainement.")
			break
		#print(f"theta0: {theta0}, theta1: {theta1}")

	with open("thetas.txt", "w") as f:
		f.write(f"{theta0} {theta1} {mini_mile} {maxi_mile} {min_price} {maxi_price}")
	
	theta0_denorm = theta0 * (maxi_price - min_price) + min_price
	theta1_denorm = theta1 * (maxi_price - min_price) / (maxi_mile - mini_mile)
	show_data(mileage_orig, prices_orig, theta0_denorm, theta1_denorm, mini_mile)
	print(f"\nModèle entraîné:")
	print(f"Theta0 (intercept): {theta0_denorm}")
	print(f"Theta1 (pente): {theta1_denorm}")

if __name__ == "__main__":
	file = "data.csv"
	train(file)