#!/usr/bin/env python

import psycopg2
from datetime import datetime

DBNAME = "news"


def db_connect():
    """
    Creates and returns a connection to the database defined by DBNAME.
    Returns:
        db - A connection to the database.
    """
    return psycopg2.connect(database=DBNAME)


def execute_query(query):
    """
    execute_query takes an SQL query as a parameter.
    Executes the query and returns the results as a list of tuples.
    args:
    query - an SQL query statement to be executed.

    returns:
    A list of tuples containing the results of the query.
    """
    db = db_connect()
    c = db.cursor()
    c.execute(query)
    r = c.fetchall()
    db.close()
    return r


#   What are the most popular three articles of all time?
def print_top_articles():
    """Prints out the top 3 articles of all time."""
    popular_articles_query = """
    SELECT title, views
    FROM hits
    ORDER BY views DESC
    LIMIT 3;
    """
    popular_articles = execute_query(popular_articles_query)
    print "MOST POPULAR ARTICLES"
    for title, views in popular_articles:
        print(u'\u2022' + ' "{}" - {} views'.format(title, views))


#   Who are the most popular article authors of all time?
def print_top_authors():
    """Prints a list of authors ranked by article views."""
    popular_authors_query = """
    SELECT authors.name, sum(hits.views) as views
    FROM authors JOIN hits
    ON authors.id = hits.author
    GROUP BY authors.name
    ORDER BY views DESC
    """
    popular_authors = execute_query(popular_authors_query)
    print "MOST POPULAR AUTHORS"
    for author in popular_authors:
        print u"\u2022 " + str(author[0]) + ' - ' + str(author[1]) + ' views'


#   On which days did more than 1% of requests lead to errors?
def print_errors_over_one():
    """Prints out the days where more than 1% of logged access
    requests were errors."""
    errors_query = """
    SELECT hitsbyday.day,
    ROUND(100*errors.num_of_errors/hitsbyday.num::numeric, 1)
    AS percentage
    FROM errors JOIN hitsbyday
    ON errors.day = hitsbyday.day
    WHERE 100*errors.num_of_errors/hitsbyday.num > 1
    """
    errors = execute_query(errors_query)
    print "DAYS WHERE MORE THAN 1% REQUESTS LEAD TO ERRORS"
    for days in errors:
        print(u'\u2022'+' {:%B %d, %Y} - {}% errors'.format(days[0], days[1]))


if __name__ == '__main__':
    print_top_articles()
    print
    print_top_authors()
    print
    print_errors_over_one()
