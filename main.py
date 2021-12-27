import regression_models
import temperature_data
from datetime import datetime

if __name__ == '__main__':
    temperature_data = temperature_data.fetch_temperature_data(1)
    regression_models.temperature_linear_regression_model(temperature_data)
