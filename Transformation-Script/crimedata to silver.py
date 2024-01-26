# Databricks notebook source
dbutils.fs.ls('/mnt/crimelake')

# COMMAND ----------

dbutils.fs.ls('/mnt/silver')

# COMMAND ----------

input_path = '/mnt/crimelake/crimeID/*'

# COMMAND ----------

df = spark.read.format('parquet').load(input_path)

# COMMAND ----------

## Generating Foriegn key values to the tables.
column_name =['Time_ID','Location_ID']
column_values = []
row_count = df.count()
time_values,location_values = [],[]
## for time_ID
for row in range(row_count):
    time_values.append(f"T{row}")
column_values.append(time_values)
#print(column_values)

## for Location_ID
for row in range(row_count):
    location_values.append(f"L{row}")
column_values.append(location_values)



##print(column_values)



# COMMAND ----------

from pyspark.sql import functions as F


# Converting the date_time to date and time
df = df.withColumn('Date', F.to_date('date_time'))
df = df.withColumn('Time', F.date_format('date_time', 'HH:mm:ss'))
df = df.drop('date_time')

#sparkDF.show()
#sparkDF.printSchema()

# COMMAND ----------

df.write.format("delta").mode("overwrite").save('/mnt/silver/crimedata/crime_silverdata')
