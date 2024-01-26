# Databricks notebook source
dbutils.fs.ls('/mnt/silver/crimedata/crime_silverdata/')

# COMMAND ----------

dbutils.fs.ls('/mnt/gold/')

# COMMAND ----------

input_path = '/mnt/silver/crimedata/crime_silverdata/'

# COMMAND ----------

df = spark.read.format('delta').load(input_path)

# COMMAND ----------

from pyspark.sql.functions import col
## creating Dimension table.
Dimension = ["Time","Crime","Location"]

Time_Dimension = df.select(*["Time_ID","Date","Year","Time"])
Crime_Dimension = df.select(*["case_number","IUCR","iucr_primary_type","iucr_description"])
Location_Dimension = df.select(*["Location_ID","block","beat","district","ward","location_description","Longitude","Latitude"])

## creating Fact Table
Incident = df.select(*["id","case_number","Time_ID","Location_ID","updated_on","arrest","domestic"])

# display(Time_Dimension)
# display(Crime_Dimension)
# display(Location_Dimension)
# display(Incident)

# COMMAND ----------

Time_Dimension.write.format("delta").mode("overwrite").save('/mnt/gold/crimedata/Time')
Crime_Dimension.write.format("delta").mode("overwrite").save('/mnt/gold/crimedata/Crime')
Location_Dimension.write.format("delta").mode("overwrite").save('/mnt/gold/crimedata/Location')
Incident.write.format("delta").mode("overwrite").save('/mnt/gold/crimedata/Incident')

