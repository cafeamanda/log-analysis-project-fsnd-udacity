#!/usr/bin/env python

import psycopg2
from datetime import datetime

db = psycopg2.connect("dbname=news")
c = db.cursor()

#   What are the most popular three articles of all time?
popular_articles_query = """
SELECT articles.title, count(log.id) AS pageview
FROM articles JOIN log
ON log.path LIKE CONCAT(\'%\', articles.slug, \'%\')
GROUP BY articles.title
ORDER BY pageview DESC
LIMIT 3
"""
c.execute(popular_articles_query)
popular_articles = c.fetchall()
print "MOST POPULAR ARTICLES"
for article in popular_articles:
    title = str(article[0])
    views = str(article[1])
    print u"\u2022" + ' "' + title + '"' + ' - ' + views + " views"
print

#   Who are the most popular article authors of all time?
popular_authors_query = """
SELECT authors.name, hits.pageview
FROM authors JOIN hits
ON authors.id = hits.author
ORDER BY hits.pageview DESC
"""
c.execute(popular_authors_query)
popular_authors = c.fetchall()
print "MOST POPULAR AUTHORS"
for author in popular_authors:
    print u"\u2022 " + str(author[0]) + ' - ' + str(author[1]) + ' views'
print

#   On which days did more than 1% of requests lead to errors?
errors_query = """
SELECT hitsbyday.day,
ROUND(100*errors.num_of_errors/hitsbyday.num::numeric, 1)
AS percentage
FROM errors JOIN hitsbyday
ON errors.day = hitsbyday.day
WHERE 100*errors.num_of_errors/hitsbyday.num > 1
"""
c.execute(errors_query)
errors = c.fetchall()
print "DAYS WHERE MORE THAN 1% REQUESTS LEAD TO ERRORS"
for days in errors:
    s = datetime.strptime(str(days[0]), '%Y-%m-%d')
    d = s.strftime('%B %d, %Y')
    print u"\u2022 " + d + ' - ' + str(days[1]) + '% errors'

db.close()
