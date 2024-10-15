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

    """finds the index of the first occurrence of a delimiter, else returns -1"""
    def find_delimiter(name):
        delimiter = [',']
        length = len(name)
        for i in range(length):
            if name[i] == delimiter[0]:
                return i
        return -1
                
    """function to remove unwanted data in the Names column"""
    def clean_name(names):
        cleaned_name = []
        additional_names = []
        additional_instrument = ''
        for name in names:
            if (pd.notnull(name) and ' only)' in name):
                first_delimiter = name.find('(')
                end_idx = name.find('only')
                additional_instrument = (name[first_delimiter+1:end_idx]).strip()
                additional_names.append(name[:first_delimiter])
            elif (pd.notnull(name) and name.lower() != "same as above" and 
                  name.lower() != "vacant" and name.lower()[:3] != "tbd" ): 
                first_delimeter = find_delimiter(name)
                name_wo_delimeter = name
                if first_delimeter != -1:
                    name_wo_delimeter = name[:first_delimeter]
                name_wo_delimeter = name_wo_delimeter.strip()
                if name_wo_delimeter not in cleaned_name:
                    cleaned_name.append(name_wo_delimeter)
        return cleaned_name, additional_names, additional_instrument
    
    percussion_instruments = {'tambourine','triangle','castanets', 'triangle', 
                              'bass drum', 'crash cymbals', 'timpani', 'glock', 
                              'snare drum', 'tri/tamb/cymbal', 'cymbals' }
    instruments_w_diff_parts = ['flute', 'oboe', 'clarinet', 'bassoon',
                                'trombone','trumpet', 'horn']
    instrument_dict = dict()

    # Read CSV file
    file_path = ['../../assets/rosters/symphony_f24_roster.csv', 
                 '../../assets/rosters/chamber_f24_roster.csv']
    columns = ['Instrument', 'Name']  # Replace with your column names
    
    # iterate and read from both symphony and chamber rosters
    for path in file_path:
        df = pd.read_csv(path, usecols=columns)  
        # Fill NaN values in 'Instrument' column with the previous value (forward fill)
        df['Instrument'] = df['Instrument'].ffill() 
        df['Instrument'] = df['Instrument'].str.lower()
        # Group by 'Instrument' and aggregate the 'Name' column as a set
        initial_dict = df.groupby('Instrument')['Name'].apply(list).to_dict()
        # add the information from initial dictionary to the instrument dictionary
        for instrument, names in list(initial_dict.items()):
            instrument_dict[instrument] = instrument_dict.get(instrument, []) + names
        
        # Clean data for instrument and names
        for instrument, names in list(instrument_dict.items()):
            key = instrument
            # Remove duplicate keys for percussion instruments
            if (instrument[:4] == "perc" and instrument != "percussion") or instrument in percussion_instruments:
                instrument_dict['percussion'] = instrument_dict.get('percussion',[]) + names
                instrument_dict.pop(instrument)
                key = 'percussion'
            # Remove duplicate keys in piccolo section
            elif 'picc' in instrument and instrument != "piccolo":
                instrument_dict['piccolo'] = instrument_dict.get('piccolo',[]) + names
                instrument_dict.pop(instrument)
                key = 'piccolo'
            else:
                # Remove duplicate keys in wind sections
                for wind in instruments_w_diff_parts:
                    if wind in instrument and wind != instrument:
                        instrument_dict[wind] = instrument_dict.get(wind,[]) + names
                        instrument_dict.pop(instrument)
                        key = wind
                        break

            # Clean the names and remove None or NaN values from the lists  
            cleaned_names, additional_names, additional_instrument = clean_name(instrument_dict[key])  
            instrument_dict[key] = cleaned_names
            if len(additional_names) > 0:
                # add the additional information to the instrument dictionary
                instrument_dict[additional_instrument] = instrument_dict[additional_instrument] + additional_names
                cleaned_additional_names, dummy1, dummy2 = clean_name(instrument_dict[additional_instrument])
                instrument_dict[additional_instrument] = cleaned_additional_names
           
    # instrument_dict contains the dictionary with instruments as keys and a list of players as values

    data = instrument_dict
    
    import json
    with open('roster.json', 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)
        # f.write(json_string)
    
    return jsonify(data)



if __name__ == '__main__':
    # app.run(port=5000)
    app.run(debug=True)