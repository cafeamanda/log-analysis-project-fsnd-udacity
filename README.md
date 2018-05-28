# Log Analysis Project
This project was built under the Udacity Full-Stack Web Developer Nanodegree Program. The object of this project is a newspaper website. The user-facing newspaper site frontend itself, and the database behind it, were already built and running. The task was to build an internal reporting tool that uses information from the database to discover what kind of articles the site's readers like.

## Project Details
This project consists of:
* A PostgreSQL data base `newsdata.sql`
* A program written in python `loganalysis.py`

You should make sure you have VirtualBox and Vagrant installed and up-to-date on your computer. Once you're all set, follow the steps bellow.

## How to run the application

1. Clone this repository into your local vagrant folder.
2. Download the database [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip) and unzip it into your local vagrant folder.
3. Bring the virtual machine online: `$ vagrant up`
4. Log into it: `$ vagrant ssh`
5. Navigate to vagrant directory: `$ cd /vagrant`

7. To load the data in the database, type: `$ psql -d news -f newsdata.sql`
8. To later connect to the database, simply type: `$ psql news`

9. Once you're connected to the database, you'll need to create 3 views.

    8.1.  Create **hits** view
    ```
    news => CREATE VIEW hits AS
      SELECT articles.author, count(log.id) as pageview
      FROM articles JOIN log
      ON log.path LIKE CONCAT('%', articles.slug, '%')
      GROUP BY articles.author;
    ```

    8.2. Create **errors** view
    ```
    news => CREATE VIEW errors AS
      SELECT DATE(time) as day, count(status) as num_of_errors
      FROM log WHERE status = '404 NOT FOUND'
      GROUP BY day
      ORDER BY day ASC;
    ```


    8.3. Create **hitsbyday** view
    ```
    news => CREATE VIEW hitsbyday AS
      SELECT DATE(time) AS day, count(id) as num
      FROM log
      GROUP BY day;
    ```

10. Hit `ctrl + d` or type in `\q` to disconnect from the database

11. `cd` to the Log Analysis Project folder and run the internal reporting tool:
    ```
    $ cd log-analysis-project-fsnd-udacity
    $ python loganalysis.py
    ```
You should be able to see the contents of Log Analysis Project/output_example.txt displayed on your terminal.
