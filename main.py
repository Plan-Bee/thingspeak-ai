import data as plan_bee_data
from datetime import datetime


if __name__ == '__main__':
    temperature_data = plan_bee_data.fetch_temperature_data(1)

    learning_data, test_data = plan_bee_data.split_data_by_timestamp(
        temperature_data=temperature_data,
        split_timestamp=split_timestamp
    )

    scaled_learning_data = plan_bee_data.preprocess_temperature_data(learning_data)
    scaled_test_data = plan_bee_data.preprocess_temperature_data(test_data)

    learning_values, learning_results = plan_bee_data.get_training_data(scaled_learning_data, prediction_days)
