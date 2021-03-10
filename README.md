# The Lucky Movie Search
### Are you feeling lucky?

This python script uses [selenium](https://www.selenium.dev/) to search [Rotten Tomatoes](rottentomatoes.com) for movies based on the user provided search string. The results are filtered and sorted and then a best match is returned. 

#### Important!
You must change the PATH variable in main.py to the location of the chromedriver on your machine 
```python
PATH = "/path/to/chrome/driver"
driver = webdriver.Chrome(PATH)

```

## Usage
This application includes a command line argument parser, run it from the command line with the string you want to search.
```bash
python main.py godfather
```
The search string is a required argument.