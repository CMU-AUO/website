import json
from flask import Flask, jsonify, request
from flask_cors import CORS

# https://www.moesif.com/blog/technical/api-development/Building-RESTful-API-with-Flask/

app = Flask(__name__)
CORS(app)
# to customize which domains are allowed to access the app
# CORS(app, resources={r"/api/*": {"origins": "http://example.com"}})

@app.route("/")
def home():
    return "Hello, api for CMU All University Orchestra!"

@app.route('/api/data')
def get_data():
    data = {'message': 'Hello from Flask API!'}
    return jsonify(data)

@app.route('/api/parsecsv')
def get_parsed_data():
    import pandas as pd

    # function to remove unwanted data in the Names column
    def clean_name(names):
        cleaned_name = []
        for name in names:
            if pd.notna(name) and name.lower() != "same as above" and name.lower()[:3] != "tbd": 
                # unique_name = name.replace("Same as above", "").replace("same as above", "").strip()
                if name not in cleaned_name:
                    cleaned_name.append(name)
        return cleaned_name
    percussion_instruments = {'tambourine','triangle','castanets', 'triangle', 
                              'bass drum', 'crash cymbals', 'timpani', 'glock', 'snare drum'}
    def aggregate_percussion(instrument, instrument_dict):
        instrument_dict['percussion'] = instrument_dict.get('percussion',[]) + names
        instrument_dict.pop(instrument)
        return instrument_dict['percussion']
    def aggregate_piccolo(instrument, instrument_dict):
        instrument_dict['piccolo'] = instrument_dict.get('piccolo',[]) + names
        instrument_dict.pop(instrument)
        return instrument_dict['piccolo']

    # Read CSV file from a folder
    file_path = '../../assets/rosters/symphony_f24_roster.csv'
    # df = pd.read_csv(file_path)
    columns = ['Instrument', 'Name']  # Replace with your column names
    df = pd.read_csv(file_path, usecols=columns)  
    # Fill NaN values in 'Instrument' column with the previous value (forward fill)
    df['Instrument'] = df['Instrument'].ffill() 
    df['Instrument'] = df['Instrument'].str.lower()
    # Group by 'Instrument' and aggregate the 'Name' column as a list
    instrument_dict = df.groupby('Instrument')['Name'].apply(list).to_dict()
    
    # Clean data for instrument and names
    for instrument, names in list(instrument_dict.items()):
        # Remove duplicate keys for percussion instruments
        if instrument[:4] == "perc" or instrument in percussion_instruments:
            instrument_dict['percussion'] = instrument_dict.get('percussion',[]) + names
            instrument_dict.pop(instrument)
            names = instrument_dict['percussion']
        # Remove duplicate keys in flute/piccolo section
        if 'picc' in instrument and instrument != "piccolo":
            instrument_dict['piccolo'] = instrument_dict.get('piccolo',[]) + names
            # instrument_dict.pop(instrument)
            del instrument_dict[instrument]
            names = instrument_dict['piccolo']
            # names = aggregate_piccolo(instrument, instrument_dict)
        # Clean the names and remove None or NaN values from the lists  
        cleaned_names = clean_name(names)  # Filter out NaN or None
        instrument_dict[instrument] = cleaned_names   
        
        
        
    # Now `instrument_dict` contains the dictionary with instruments as keys and a list of players as values
    print(instrument_dict)

    data = {'message': 'parsing csv'}
    # need a dictionary with keys being the Instrument name,
    # with values being a list of player names that play this instrument
    return jsonify(data)


if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)