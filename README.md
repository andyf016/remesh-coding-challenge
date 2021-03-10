# The Lucky Movie Search
### Are you feeling lucky?

This python script uses [selenium](https://www.selenium.dev/) to search [Rotten Tomatoes](rottentomatoes.com) for movies based on the user provided search string. The results are filtered and sorted and then a best match is returned. 

### Important!
You must change the PATH variable in main.py to the location of the chromedriver on your machine 
```python
PATH = "/path/to/chrome/driver"
driver = webdriver.Chrome(PATH)

```
### Requirements
install the required packages in your virtual environment:
```bash
python -m pip install -r requirements.txt
```


## Usage
This application includes a command line argument parser, run it from the command line with the string you want to search.
```bash
python main.py godfather
```
The search string is a required argument.

## Bug!
There is a recurring stale element refrence exception occuring while navigating the pages of results. After several failed attempts to fix the root cause of the issue I included a time.sleep() function. This helps mitigates the issue but it is not a complete fix. Any feedback regarding this issue and how to fix it would be greatly appreciated. 