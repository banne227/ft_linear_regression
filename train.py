import math

learning_rate = 0.0001
iterations = 1000

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

def estimate_price(mileage, theta0, theta1):
    return theta0 + (theta1 * mileage)

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
	
	mini_mile = min(mileage)
	maxi_mile = max(mileage)
	for i in range(len(mileage)):
		mileage[i] = (mileage[i] - mini_mile) / (maxi_mile - mini_mile)
	
	maxi_price = max(prices)
	min_price = min(prices)
	for i in range(len(prices)):
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
		print(f"theta0: {theta0}, theta1: {theta1}")

	with open("thetas.txt", "w") as f:
		f.write(f"{theta0} {theta1}")

if __name__ == "__main__":
	file = "data.csv"
	train(file)