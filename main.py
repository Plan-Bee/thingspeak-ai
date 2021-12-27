import data as plan_bee_data
from datetime import datetime

prediction_days = 13
split_timestamp = datetime.strptime('2021-10-01', '%Y-%m-%d')

if __name__ == '__main__':
    temperature_data = plan_bee_data.fetch_temperature_data(1)

	training_data, test_data = plan_bee_data.split_data_by_timestamp(
		temperature_data=temperature_data,
		split_timestamp=split_timestamp
	)

	scaled_learning_data = plan_bee_data.preprocess_temperature_data(training_data)
	scaled_test_data = plan_bee_data.preprocess_temperature_data(test_data)

	training_values, training_results = plan_bee_data.split_preprocessed_data(scaled_learning_data)
	test_values, test_results = plan_bee_data.split_preprocessed_data(scaled_learning_data)

	training_results = np.array(training_results)
	training_values = reformat_list(training_values)
	test_values = reformat_list(test_values)

	# Build The Model
	model = Sequential()

	model.add(LSTM(units=100, return_sequences=True, input_shape=(training_values.shape[0], 1)))
	model.add(Dropout(0.2))
	model.add(LSTM(units=100, return_sequences=True))
	model.add(Dropout(0.2))
	model.add(LSTM(units=100))
	model.add(Dropout(0.2))
	model.add(Dense(units=1))  # Prediction of the next closing value

	model.compile(optimizer='adam', loss='mean_squared_error')
	model.fit(training_values, training_results, epochs=2, batch_size=32)

	prediction = model.predict(test_values)

	print(prediction)
	print(plan_bee_data.reverse_transform_scaled_data(prediction))
