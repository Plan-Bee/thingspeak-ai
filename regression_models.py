"""
Different regression models to evaluate the hive and outdoor temperature data
"""
from datetime import datetime

import pandas as pd
import tensorflow as tf
from matplotlib import pyplot as plt
from tensorflow.keras import layers

from temperature_data import split_temperature_data, normalize_temperature_data, plot_loss, plot_temperature


def temperature_linear_regression_model(temperature_data: [(int, int, datetime)]):
	"""
	Calculates a linear regression line between the hive and outdoor temperature
	:param temperature_data: The temperature data to use for the training
	"""
	# 1. fetch and split data
	test_features, test_labels, train_features, train_labels = split_temperature_data(temperature_data)
	# 2. normalize data for further processing
	outdoor_temp_normalizer = normalize_temperature_data(train_features)
	# 3. TODO research on Sequential model
	outdoor_temp_model = tf.keras.Sequential([
		outdoor_temp_normalizer,
		layers.Dense(units=1)
	])
	# 4. Finishing the model by giving an optimizer and loss function
	outdoor_temp_model.compile(
		optimizer=tf.optimizers.Adam(learning_rate=0.1),  # Adam gradient algorithm
		loss='mean_absolute_error'
	)
	# 5. Initialize params for loss plot
	history = outdoor_temp_model.fit(
		train_features['outdoor_temperature'],  # input
		train_labels,  # output
		epochs=100,
		verbose=0,
		# Calculate validation results on 20% of the training data.
		validation_split=0.2
	)

	hist = pd.DataFrame(history.history)
	hist['epoch'] = history.epoch

	plot_loss(history)
	plt.show()
	# 6. Shows how good our model performs
	test_results = {
		'outdoor_temp_model': outdoor_temp_model.evaluate(
			test_features['outdoor_temperature'],
			test_labels, verbose=0)
	}
	print(test_results)
	# 7. Params for plot visualization
	x = tf.linspace(-10.0, 40, 51)
	y = outdoor_temp_model.predict(x)
	# 8. Show Plot
	plot_temperature(x, y, train_features, train_labels)
	plt.show()
