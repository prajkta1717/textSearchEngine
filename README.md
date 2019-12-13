# Text Search Engine for Trending Videos on Youtube
<b>Classification of Videos</b>
Search a trending video by putting name in Search box.</br>

Required libraries:</br>
pip install flask</br>
pip install nltk.stem</br>
pip install re</br>
pip install nltk.corpus</br>

Steps to run and deploy in localhost</br>
1. Install flask in your environment.
2. Download this repo to a folder
3. Navigate upto the 'PracticeProjectDM' directory
4. from a console run the textSearchUI.py file by the command **python3.6 textSearchUI.py**
5. Hit **localhost:5000** in browser.

textSearchUI.py Entry point of the front end. Handles the search request and update the UI with results.</br>
frontend.py is to calculate TF-IDF of all the words of dataset and stores the data in TF-IDF4.txt file.</br>
templates contains search request, search result and error UI file.
