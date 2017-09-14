#!/usr/bin/env python3
#
# The source code of fullstack web developer project 3

import psycopg2
import datetime

def connect_db(dbname):
    try:
        conn = psycopg2.connect("dbname={}".format(dbname))
        cur = conn.cursor()
        return conn, cur
    except:
        sys.exit(1)

def find_most_popular3articles():
    # SQL for finding the most popular 3 articles
    most_popular3articles_sql = """
    select articles.title, slug_count.num
    from articles
    join (
        select substring(path, 10) as slug, count(*) as num
        from log
        where path like '/article/%' and status = '200 OK'
        group by path
        order by num desc
        limit 3
    ) as slug_count
    on articles.slug = slug_count.slug
    order by slug_count.num desc
    """

    conn, cur = connect_db("news")
    cur.execute(most_popular3articles_sql)
    popular3articles = cur.fetchall()
    conn.close()

    print("The most popular three articles are as follows:")
    for article in popular3articles:
        print("\"{}\" -- {} views".format(article[0], article[1]))

def find_most_popular_article_authors():
    # SQL for the most popular article authors of all time
    most_popular_article_authors_sql = """
    select authors_articles.name, count(*) as num
    from (
        select a.id, a.name, articles.slug
        from authors a left join articles
        on a.id = articles.author
        order by a.id asc
    ) as authors_articles join log
    on authors_articles.slug = substring(log.path, 10)
    where log.path like '/article/%' and log.status = '200 OK'
    group by authors_articles.name
    order by num desc
    """

    conn, cur = connect_db('news')
    cur.execute(most_popular_article_authors_sql)
    authors_views = cur.fetchall()
    conn.close()

    print("\nThe most popular article authors are as follows:")
    for author_view in authors_views:
        print("{} -- {} views".format(author_view[0], author_view[1]))

def find_error_days():
    # SQL for doys which have > 1% of requests lead to errors
    # One more layer of select is required because error_per cannot be referenced
    # inside the subquery as where happens select
    sql = """
    select time::date, round(error_per::decimal, 1) from
    (
        select error_count.time, (error_count.num::float / total_count.num * 100) as error_per -- # NOQA
        from (
            select date_trunc('day', time) as time, count(*) as num
            from log
            where status != '200 OK'
            group by date_trunc('day', time)
            order by date_trunc('day', time) desc
        ) as error_count
        join
        (
            select date_trunc('day', time) as time, count(*) as num
            from log
            group by date_trunc('day', time)
            order by date_trunc('day', time) desc
        ) as total_count
        on error_count.time = total_count.time
    ) as tmp
    where error_per > 1;
    """

    conn, cur = connect_db('news')
    cur.execute(sql)
    error_days = cur.fetchall()
    conn.close()

    print("\nDays which have > 1% of requests lead to errors are as follows:")
    for error_day in error_days:
        date = error_day[0].strftime('%b %d, %Y')
        print(date, "--", str(error_day[1]) + "% errors")

if __name__ == '__main__':
    find_most_popular3articles()
    find_most_popular_article_authors()
    find_error_days()
