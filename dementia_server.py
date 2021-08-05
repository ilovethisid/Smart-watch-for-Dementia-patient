from flask import Flask, render_template, request
from db_manager import DatabaseManager

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def handle_request():
    return "dementia server"


@app.route('/append-location', methods=['POST'])
def handle_gps_location_set():
    if request.is_json:
        params = request.get_json()
        print(params['longitude'], params['latitude'])
        my_db = DatabaseManager().instance()
        my_db.create_connection()
        my_db.get_cursor()
        my_db.close_connection()
        return 'ok'
    return 'failed'


@app.route('/query-location', methods=['GET', 'POST'])
def query_patient_location():
    my_db = DatabaseManager().instance()
    my_db.create_connection(DatabaseManager.DB_WATCH_DATA)
    my_db.get_cursor()
    longitude = my_db.select_last_element_of_column("SmartWatch", "longitude")
    latitude = my_db.select_last_element_of_column("SmartWatch", "latitude")
    my_db.close_connection()
    test_str = str(longitude, latitude)
    return test_str



@app.route('/address', methods=['GET', 'POST'])
def address_request():
    return render_template("daum.html")


app.run(host="0.0.0.0", port=5000, debug=True)