import array
from sklearn.preprocessing import MinMaxScaler
from datetime import datetime
import sql_connection_handler as db_handler

KELVIN_OFFSET = 273.15

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

def wir_schauen_einfach_mal(temperature_data: [(int, int, datetime)]):
    dataset = pd.DataFrame(temperature_data)

    dataset.columns = ['broodroom_temperature', 'outdoor_temperature', 'time']

def split_data_by_timestamp(temperature_data: [], split_timestamp: datetime) -> ([], []):
    learning_data = []
    test_data = []

    for broodroom_temperature, outdoor_temperature, timestamp in temperature_data:
        if timestamp <= split_timestamp:
            learning_data.append([broodroom_temperature, outdoor_temperature])
        else:
            test_data.append([broodroom_temperature, outdoor_temperature])

    return learning_data, test_data


def preprocess_temperature_data(temperature_data: [tuple], use_kelvin=True) -> array:
    data_to_scale = []

    if use_kelvin:
        for temperature_list in temperature_data:
            data_to_scale.append([temperature_list[0] + KELVIN_OFFSET, temperature_list[1] + KELVIN_OFFSET])
    else:
        data_to_scale.extend(temperature_data)

    scaled_data = scaler.fit_transform(data_to_scale)

    return scaled_data


def get_training_data(scaled_data, prediction_days):
    training_values = []  # input
    training_results = []  # desired output

    for x in range(prediction_days, len(scaled_data)):
        training_values.append(scaled_data[x - prediction_days:x])
        training_results.append(scaled_data[x, 0])

    return training_values, training_results


def fetch_temperature_data(id: int) -> [tuple]:
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
        hive_id = %s
    """

    cur.execute(select_temperature_data, id)
    temperature_data = cur.fetchall()

    return temperature_data
