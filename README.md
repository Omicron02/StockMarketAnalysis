# Introduction
## Description
6th semester Database Technologies (UE20CS343) Miniproject - Stock Market Analysis

The project uses an API provided by https://site.financialmodelingprep.com/developer/docs to stream data to the program.

It takes data of 5 different companies: Apple, Google, Microsoft, NVIDIA, Meta from the API every 2 minutes and stores it in a MySQL database. It uses a 6 minute window, i.e. it finds the min, max, avg of the data received every 6 minutes and stores it into a different table.

This data is then displayed on a streamlit UI in the form of matplotlib graphs. 

It supports batch processing and stream processing.
* <b> Batch</b>: Takes all the data stored in the database and displays min, max and avg.
* <b>Stream</b>: Takes the latest data from the database and plots it onto a graph.

It uses Kafka Streming, Spark Streaming, Zookeeper, MySQL and Streamlit.

## Basic Program Flow

![dbt_flow](https://user-images.githubusercontent.com/52106611/234940036-0af22331-98e1-4873-a20b-d92e6bbc9326.png)

# Working and Execution

## Requirements
### The brackets show the versions used in this project.
* Java (17.0.6) <img src="https://user-images.githubusercontent.com/52106611/234960006-16fd4640-04cb-49f3-a688-e7788619fde6.png" width="35">
* Scala (2.12)  <img src="https://user-images.githubusercontent.com/52106611/234959491-ad2232c1-3a52-41b7-acec-96d25eb2182e.png" width="20">
* Python (3.11.2) <img src="https://user-images.githubusercontent.com/52106611/234959157-011efd84-0b1b-47fa-a51f-bfc5bed8114e.png" width="25">
* Xampp Server (8.2.4-0) <img src="https://user-images.githubusercontent.com/52106611/234958552-c73b4ae1-f578-414c-8357-a38ac5fd5fa1.png" width="25">
* Spark (3.4.0) <img src="https://user-images.githubusercontent.com/52106611/234957673-ac579aac-0cf0-4c16-ab28-db61680030c3.png" width="40">
* Zookeeper (3.8.0)  <img src="https://user-images.githubusercontent.com/52106611/234960200-8c408ba7-ee7f-4830-a768-e2e0721d875f.png" width="20">
* Kafka (3.4.0)  <img src="https://user-images.githubusercontent.com/52106611/234960486-00ad1519-de43-499b-9e92-dc6222562e21.png" width="20">
* Python modules to pip install: streamlit, matplotlib, mysql-connector-python, dotenv, kafka-python, pyspark.

Note: Highly recommended to run on Linux, other operating systems have a lot of problems.

## Running

Assuming zookeeper and kafka are properly configured and added to path in .bashrc, run `zookeeper-server-start.sh <path_to_zookeeper_installation>/kafka_2.12-3.4.0/config/zookeeper.properties`, replace <path_to_zookeeper_installation> with the path of the zookeeper installation. In the above command, regarding kafka_2.12-3.4.0, 2.12 is the Scala version and 3.4.0 is the kafka version.

Then in a new terminal run `kafka-server-start.sh <path_to_kafka_installation>/kafka_2.12-3.4.0/config/server.properties`. 
Make sure to never close the terminals with zookeeper and kafka.

Assuming that xampp has been installed into the default directory /opt, run `sudo /opt/lampp/xampp start`.

Open ur browser and head to localhost/phpmyadmin to make sure the MySQL server is running.

Create a database 'stock' and create two tables:
* simple_data - symbol varchar(4), name varchar(30), price float, volume int, tstamp timestamp.
* agg_data - symbol varchar(4), start_time timestamp, end_time timestamp, price_avg float, price_min float, price_max float, volume_avg float, volume_min int, volume_max int, cnt int.

Note: Order of columns matter, don't change them.

Open a new terminal and run `kafka-topics.sh --create --topic simple_data --bootstrap-server localhost:9092`, then run `kafka-topics.sh --create --topic agg_data --bootstrap-server localhost:9092` and `kafka-topics.sh --create --topic insert_data --bootstrap-server localhost:9092`

Now enter the directory containing the repo and run `python3 consumer.py simple_data`.

Open a new terminal and run `python3 consumer.py agg_data`.

Open a new terminal and run `spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.4.0 sparkstream.py insert_data`. Again, the `spark-sql-kafka-0-10_2.12:3.4.0` refers to the scala version and kafka version. 

Open a new terminal and run `python3 producer.py insert_data`.

Open a new terminal and run `streamlit run lit.py`.

Enjoy!

# Credits

### * [Nirav Antony](https://github.com/Nirav-Antony) - PES2UG20CS227
### * [Rahul Samal](https://github.com/Omicron02) - PES2UG20CS262
### * [Riya Hurtis](https://github.com/rmhurtis) - PES2UG20CS277
### * [Shafiudeen Kameel](https://github.com/rmhurtis) - PES2UG20CS320










