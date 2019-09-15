# TruthSeeker
HackYeah 2019 Ringier Axel Springer articles analisis

# REST api documentation

POST `/article`
Ask for article rate
```
    {
        "title": ""
        "publication_date": ""
        "domain": ""
    }
```
Returns
```
    {
        "is_objective": is_manipulative(args['title']),
        "is_too_old": is_too_old(args['publication_date']),
        "opposition_articles": [<link>, <link>]
        "feedback_token": "<token>"
    }
```
---------------------
GET `/feedback/<token>/<rate>/` where <rate> is "up" or "down" <br/>
returns code 200 if ok 403 if wrong token


