## Description
This is the official website for the Carnegie Mellon All University Orchestra.

## Backend
The backend is built using Flask and runs on a virtual environment. 
When running the virtual environment, there should be a (.venv) in your terminal.
To enable the virtual environment, run ```source .venv/bin/activate``` for macOS.

To run the Flask app, you need to install Flask and Pandas by running the following commands: 
```pip install flask```
```pip install flask-cors```
```pip install pandas```

## Process to update member roster
1. Put the new roster.csv file(s) in the /assets/rosters folder. The first line of the csv file should be ```Piece Title,Instrument,Name,Stand (strings only)```. See previous files for reference.
2. Update ```file_path``` in /backend/api/app.py to only include the roster.csv file(s) that you've added. If there are other instruments that fit into the "percussion" instruments section, update ```percussion_instruments``` in app.py to include those instruments.
3. Inside the ```fetchData()``` function in js/scripts/js, change ```fetch(json_file_path)``` to ```fetch(api_endpoint)```. 
4. In the terminal, ```cd backend/api```, then run ```python app.py``` to start the Flask app. If this didn't work, try ```python3 app.py```.
5. Open the concerts.html page in your browser, and check to see that the member information is updated.
6. Go back to the terminal and stop the Flask app by closing the terminal or using ctr c for mac.
7. Open the backend/api/roster.json file to see if there is anything that you want to manually edit. This json file contains the data parsed from the csv files. Remember to save after making edits.
8. Inside the ```fetchData()``` function in js/scripts/js, change ```fetch(api_endpoint)``` back to ```fetch(jason_file_path)```, so that the website reads from the roster.json file.

## How to build
When you git add, git commit, git push to the gh-pages branch, the website will be updated automatically. However, if you run into build errors, it could be due to updated requirements for the backend. In this case, run ```pip freeze > requirements.txt``` in the terminal to create a requirements.txt file, then push to GitHub.