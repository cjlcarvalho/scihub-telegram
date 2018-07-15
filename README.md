# scihub-telegram

### Description:

Telegram Bot to scrap files from Sci-Hub. Made for study purposes, specially to understand Telegram bot API.

### Requirements:

- python3

- lxml

- requests

### Installing and using

- `pip install -r requirements.txt`

- Change TOKEN string in settings.py and insert your bot's token there.

- Add more available Sci-Hub URLs in (scihub-urls)[scihubbot/scihub-urls.txt] file.

- `python main.py`
    
### Commands

- `/byname article-name`
    - Command to search article by its name and download.
      
- `/download scihub-default-search`
    - Command to search article by scihub default parameters (i.e. URL, PMID/DOI or search string).
