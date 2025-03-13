
from pyspark.sql.types import *
from pyspark.sql import SparkSession

mongo_landing_db = "Landing"
income_lookup_district = "income_lookup_district"
income_lookup_neighborhood = "income_lookup_neighborhood"
rent_lookup_district = "rent_lookup_district"
rent_lookup_neighborhood = "rent_lookup_neighborhood"
opendata_income = "income_opendata"


def close_mongo_connection(db_client):
    db_client.close()


def create_spark_conn():
    spark = SparkSession \
        .builder \
        .master(f"local[*]") \
        .appName("myApp") \
        .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
        .getOrCreate()
    return spark


def get_table_as_rdd(spark, name):
    lookup_rdd = spark.read.format("mongo") \
        .option('uri', f"mongodb://localhost:27017/landing.{name}") \
        .load() \
        .rdd \
        .cache()
    return lookup_rdd


def combine_lookups(spark):
    lookup_neigh_rdd = get_table_as_rdd(spark, "income_lookup_neighborhood")
    lookup_district_rdd = get_table_as_rdd(spark, "income_lookup_district")
    # Extract the necessary fields from lookup_district_rdd
    district_id_rdd = lookup_district_rdd.flatMap(
        lambda row: [(neighborhood_id, (row._id, row.district_reconciled, row.district)) for neighborhood_id in
                     row.neighborhood_id])
    # Join lookup_neigh_rdd with district_id_rdd
    joined_rdd = lookup_neigh_rdd.map(lambda row: (row._id, row)).join(district_id_rdd)
    # Create the final RDD with the desired fields
    result_rdd = joined_rdd.map(lambda row: Row(id_neighborhood=row[1][0]._id,
                                                neighborhood=row[1][0].neighborhood,
                                                neighborhood_name=row[1][0].neighborhood_name,
                                                neighborhood_reconciled=row[1][0].neighborhood_reconciled,
                                                id_district=row[1][1][0],
                                                district_reconciled=row[1][1][1],
                                                district=row[1][1][2]))
    # result_rdd = joined_rdd.map(lambda row: (*row[1][0], *row[1][1]))
    return result_rdd


def check_missing_in_income(income_rdd, field):
    # Create an RDD that contains only the rows that have the neigh_name field
    has_neigh_name_rdd = income_rdd.filter(lambda row: 'neigh_name ' in row)
    # Create an RDD that contains only the rows that do not have the neigh_name field
    no_neigh_name_rdd = income_rdd.filter(lambda row: 'neigh_name ' not in row)
    # Count the number of rows in each RDD
    has_neigh_name_count = has_neigh_name_rdd.count()
    no_neigh_name_count = no_neigh_name_rdd.count()
    has_missing = False
    print(f"Number of rows with neigh_name: {has_neigh_name_count}")
    print(f"Number of rows without neigh_name: {no_neigh_name_count}")
    if no_neigh_name_count == 0:
        print("There are no elements with missing neigh_name")
    else:
        print(f"There are {no_neigh_name_count} rows without neigh_name")
        has_missing = True
    return has_missing


def check_repeated_income(income_rdd):
    # Create a new RDD that contains tuples of (district_name, 'neigh_name ')
    name_rdd = income_rdd.map(lambda row: (row.district_name, row['neigh_name ']))
    distinct_count = name_rdd.distinct().count()
    original_count = name_rdd.count()
    has_repeated = False
    if original_count > distinct_count:
        print("The income RDD has repeated elements.")
        has_repeated = True
    else:
        print("The income RDD does not have repeated elements.")
    return has_repeated


def create_income_rdd(spark, combined_lookups):
    income_rdd = get_table_as_rdd(spark, "income_opendata")
    # Create a new RDD where each element is a tuple of the key and the original row
    keyed_rdd1 = income_rdd.map(lambda row: ((row.district_name, row['neigh_name ']), row))
    print(keyed_rdd1.count())
    # Do the same for the second RDD
    keyed_rdd2 = combined_lookups.map(lambda row: ((row.district, row.neighborhood), row))
    print(keyed_rdd2.count())
    # Join the two RDDs based on the key
    joined_rdd = keyed_rdd1.join(keyed_rdd2).cache()
    print(joined_rdd.count())
    transformed_rdd = joined_rdd.map(lambda row: Row(_id=row[1][0]._id,
                                                     neigh_name=row[1][0]['neigh_name '],
                                                     district_id=row[1][0].district_id,
                                                     district_name=row[1][0].district_name,
                                                     info=row[1][0].info,
                                                     district_id_reconciled=row[1][1].id_district,
                                                     district_reconciled=row[1][1].district_reconciled,
                                                     neighborhood_name_reconciled=row[1][1].neighborhood_reconciled,
                                                     neighborhood_id_reconciled=row[1][1].id_neighborhood))
    return transformed_rdd


def save_income_formatted(rdd_transformed):
    transformed_df = rdd_transformed.toDF()
    transformed_df.write \
        .format("com.mongodb.spark.sql.DefaultSource") \
        .mode("overwrite") \
        .option('uri', f"mongodb://localhost:27017/formatted.income_opendata") \
        .save()



spark = create_spark_conn()
lookups_combined = combine_lookups(spark)
transformed_income = create_income_rdd(spark, lookups_combined)
save_income_formatted(transformed_income)
