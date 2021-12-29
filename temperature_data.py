"""
Fetches data from the sql database, processes it and runs an trains the ai model
"""
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import tensorflow as tf
from datetime import datetime
import sql_connection_handler as db_handler

np.set_printoptions(precision=3, suppress=True)

KELVIN_OFFSET = 273.15


def fetch_temperature_data(hive_id: int) -> [(int, int, datetime)]:
	"""
	Retrieves the temperature data from the sql database and returns the list of data tuples
	:param hive_id: The hive to retrieve temperature data for
	:return: The list of tuples containing the broodroom temperature, outdoor temperature and timestamp
	"""
	conn = db_handler.get_db_connection()
	cur = conn.cursor()

	select_temperature_data = """
	SELECT 
		broodroom_temperature,
		outdoor_temperature,
		timestamp 
	FROM 
		honeypi_data 
	WHERE 
		hive_id = %s AND
		broodroom_temperature <= 100 AND
		outdoor_temperature <= 100
	"""

	cur.execute(select_temperature_data, hive_id)
	temperature_data = cur.fetchall()

	return temperature_data


def add_kelvin_offset(temperature_data: [(int, int, datetime)]) -> [(int, int, datetime)]:
	"""
	Adds the kelvin offset to normalize the raw data for future processing
	:param temperature_data: the raw temperature data entries
	:return: List of modified temperature entries
	"""
	for broodroom_temperature, outdoor_temperature, timestamp in temperature_data:
		broodroom_temperature += KELVIN_OFFSET
		outdoor_temperature += KELVIN_OFFSET


def split_temperature_data(temperature_data: [(int, int, datetime)]):
	"""
	Transforms the raw data into a pandas dataframe and splits it into test and training data
	:param temperature_data: The raw data from the database
	:return:
	"""
	dataset = pd.DataFrame(temperature_data)
	dataset.columns = ['broodroom_temperature', 'outdoor_temperature', 'time']

	sns.pairplot(dataset[['broodroom_temperature', 'outdoor_temperature', 'time']], diag_kind='kde')
	plt.show()

	# Split data
	train_dataset = dataset.sample(frac=0.8, random_state=0)
	test_dataset = dataset.drop(train_dataset.index)

	train_features = train_dataset.copy()
	test_features = test_dataset.copy()
	train_labels = train_features.pop('broodroom_temperature')
	test_labels = test_features.pop('broodroom_temperature')

	return test_features, test_labels, train_features, train_labels


def normalize_temperature_data(train_features):
	outdoor_temperature = np.array(train_features['outdoor_temperature'])
	outdoor_temp_normalizer = tf.keras.layers.Normalization(input_shape=[1, ], axis=None)
	outdoor_temp_normalizer.adapt(outdoor_temperature)
	return outdoor_temp_normalizer


def plot_loss(history):
	plt.plot(history.history['loss'], label='loss')
	plt.plot(history.history['val_loss'], label='val_loss')
	plt.ylim(0.5, 1.5)
	plt.xlabel('Epoch')
	plt.ylabel('Error [broodroom_temperature]')
	plt.legend()
	plt.grid(True)


def plot_temperature(x, y, train_features, train_labels):
	plt.scatter(train_features['outdoor_temperature'], train_labels, label='Data')
	plt.plot(x, y, color='k', label='Predictions')
	plt.xlabel('Outdoor')
	plt.ylabel('Indoor')
	plt.legend()
