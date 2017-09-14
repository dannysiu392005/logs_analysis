# Logs Analysis Project
This repo is the source code of the Full Stack Web Developer Nanodegree Project
III - Logs Analysis Project

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
