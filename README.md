# Logs Analysis Project
This repo is the source code of the Full Stack Web Developer Nanodegree Project
III - Logs Analysis Project

# Explanation of each SQL query
1. SQL for finding the most popular 3 articles
    ``` sql
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
    ```
    - The valid path of an article is always something like
      `/article/article-slug` so we have `path like '/article/%'` and use
substring of the path for comparison (`substring(path, 10)`)
    - In order to make sure the request is valid, we need the status code to be
      `200 OK`
    - And we want the most popular 3 articles, so need order by `num` in
      descending order and `limit 3`
    - Finally, perform an inner join to obtain the answer

2. SQL for the most popular article authors of all time
    ``` sql
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
    ```
    - The subquery helps find the author of each article with the corresponding
      slug
    - Then we perform an inner join to find the view obtained by each author to
      find the anser
    
3. SQL for doys which have > 1% of requests lead to errors
One more layer of select is required because error_per cannot be referenced
inside the subquery as where happens select
    ``` sql
    select time::date, round(error_per::decimal, 1) from
    (
        select error_count.time, (error_count.num::float / total_count.num * 100) as error_per
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
    ```
    - `date_trunc` helps truncate the timestamp with timezone to day only
    - The first subquery finds the number of invalid requests per day
    - The second subquery finds the number of requests per day
    - The join helps find the corresponding number of invalid requests per day
      of the number of requests per day and hence the answer
    - There is an outer layer `select` because error_per cannot be referenced as
      where happens before select

# How to run the project (on a mac)
- You need to install `vagrant` and `VirtualBox` (Please refer other online
  resources yourself)
    - Make sure your your vm includes `python3` and `psql`
- Load data
    - Download the data
      [here](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip)
    - Unzip it and put `newsdata.sql` into the `vagrant` directory, which is
      shared with your vm
    - Inside the vm, type `psql` to enter the PostgreSQL server
    - Create a database
    - Type `\q` to quite
    - On the terminal, type `psql -d [database name] -f newsdata.sql` to load
      the data
- Run `log_analysis.py` by typing `python3 log_analysis.py`, you will see an
  output which is the same as the one in `example_output.txt`

# License
This project is released under the [MIT
License](https://opensource.org/licenses/MIT).
