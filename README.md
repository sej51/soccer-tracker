# soccer-tracker

*Please keep in mind for testing we are using a free API and are only allowed a few requests per minute. The API takes a minute to reload.

## URL Link to Access

https://soccer-tracker.onrender.com

## Setup

Create a virtual environment (first time only):

```sh
conda create -n soccer-tracker python=3.10
```

Activate the environment:

```sh
conda activate soccer-tracker
```

Install packages:

```sh
pip install -r requirements.txt
```

[Obtain an API Key](https://sendgrid.com/en-us/solutions/email-api) from SendGrid.

[Obtain an API Key](https://www.football-data.org/) from Football Data.

Create a ".env" file and add contents like the following (using your own SendGrid API Key and Football Data API Key):

```sh
# this is the ".env" file:
API_TOKEN="..."
SENDGRID_API_KEY = "..."
SECRET_KEY="..."
```


## Web App
Run the web app (then view in the browser at http://localhost:5000/):

```sh
# Mac OS:
FLASK_APP=app flask run

# Windows OS:
# ... if `export` doesn't work for you, try `set` instead
# ... or set FLASK_APP variable via ".env" file
export FLASK_APP=app
flask run
```


## Testing

Run tests:

```sh
pytest
```


## Code Climate

This project uses Code Climate for automated code quality analysis.

Setting Up Code Climate:

1. Sign up for [Code Climate](https://codeclimate.com/quality) if you haven’t already.
2. Add the repository to your Code Climate dashboard.
