# Schoology Web Controller
A Selenium-based web controller for Schoology.

## Installation
``pip install git+https://github.com/GitPushPullLegs/schoologywebcontroller.git``

##Quick Start
```python
from schoologywebcontroller import SchoologyController

client = SchoologyController(show_window=True, download_path='optional/download/path')
client.login(username='username', password='password',
             school='School Name', school_id=324543)
client.request_usage(start_date='02/20/2021', end_date='02/20/2021')
# After you retrieve the link to the download
client.download_usage(link='thelinkthatwasemailedtoyou.com')
```

**If you don't know your school ID run do the following to export**
```python
from schoologywebcontroller import SchoologyController

client = SchoologyController(show_window=True, download_path='optional/download/path')
client.login(username='username', password='password',
             school='School Name', school_id=324543)
client.export_nids_to_csv(school='School Name', outfile_path='path/to/export.csv')
```