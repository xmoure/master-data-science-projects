from pyspark.sql import SparkSession
from pyspark.sql.types import *

spark = SparkSession \
    .builder \
    .master(f"local[*]") \
    .appName("myApp") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
    .getOrCreate()

lookup = spark.read.format("mongo") \
    .option('uri', f"mongodb://localhost:27017/landing.income_lookup_neighborhood") \
    .load() \
    .rdd \
    .cache()


def get_table_as_rdd(name):
    lookup_rdd = spark.read.format("mongo") \
        .option('uri', f"mongodb://localhost:27017/landing.{name}") \
        .load() \
        .rdd \
        .cache()
    return lookup_rdd


def combine_lookups():
    lookup_neigh_rdd = get_table_as_rdd("income_lookup_neighborhood")
    lookup_district_rdd = get_table_as_rdd("income_lookup_district")
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


def create_transformed_rdd():
    cultural = spark.read.format("mongo") \
        .option('uri', 'mongodb://localhost:27017/landing.equipaments_cultura') \
        .load() \
        .rdd \
        .cache()
    lookups_combined = combine_lookups()
    # Create a new RDD where each element is a tuple of the key and the original row

    keyed_rdd1 = cultural.map(
        lambda x: ((x["addresses_district_name"].lower(), x["addresses_neighborhood_name"].lower()), x) if x[
                                                                                                               "addresses_neighborhood_name"] is not None else None).filter(
        lambda x: x is not None)

    print(keyed_rdd1.count())
    # Do the same for the second RDD
    keyed_rdd2 = lookups_combined.map(lambda row: ((row.district.lower(), row.neighborhood.lower()), row))

    print(keyed_rdd2.count())
    # Join the two RDDs based on the key
    joined_rdd = keyed_rdd1.join(keyed_rdd2).cache()
    print(joined_rdd.count())
    transformed_rdd = joined_rdd.map(lambda row: Row(
        neighborhood_id_reconciled=row[1][1][0],
        district_id_reconciled=row[1][1][4],
        district_reconciled=row[1][1][5],
        neighborhood_name_reconciled=row[1][1][3],
        addresses_district_id=row[1][0].addresses_district_id,
        addresses_district_name=row[1][0].addresses_district_name,
        addresses_end_street_number=row[1][0].addresses_end_street_number,
        addresses_main_address=row[1][0].addresses_main_address,
        addresses_neighborhood_id=row[1][0].addresses_neighborhood_id,
        addresses_neighborhood_name=row[1][0].addresses_neighborhood_name,
        addresses_road_id=row[1][0].addresses_road_id,
        addresses_road_name=row[1][0].addresses_road_name,
        addresses_start_street_number=row[1][0].addresses_start_street_number,
        addresses_town=row[1][0].addresses_town,
        addresses_zip_code=row[1][0].addresses_zip_code,
        created=row[1][0].created,
        geo_epgs_25831_x=row[1][0].geo_epgs_25831_x,
        geo_epgs_25831_y=row[1][0].geo_epgs_25831_y,
        geo_epgs_4326_x=row[1][0].geo_epgs_4326_x,
        institution_name=row[1][0].institution_name,
        institution_id=row[1][0].institution_id,
        modified=row[1][0].modified,
        name=row[1][0].name,
        register_id=row[1][0].register_id,
        secondary_filters_asia_id=row[1][0].secondary_filters_asia_id,
        secondary_filters_fullpath=row[1][0].secondary_filters_fullpath,
        secondary_filters_id=row[1][0].secondary_filters_id,
        secondary_filters_name=row[1][0].secondary_filters_name,
        secondary_filters_tree=row[1][0].secondary_filters_tree,
        values_attribute_id=row[1][0].values_attribute_id,
        values_attribute_name=row[1][0].values_attribute_name,
        values_category=row[1][0].values_category,
        values_description=row[1][0].values_description,
        values_id=row[1][0].values_id,
        values_outstanding=row[1][0].values_outstanding,
        values_value=row[1][0].values_value,
    ))
    return transformed_rdd


joined_rdd = create_transformed_rdd()
#print(joined_rdd.count())
joined_df = joined_rdd.toDF()
joined_df.write \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .mode("overwrite") \
    .option('uri', f"mongodb://localhost:27017/formatted.cultural_equipment") \
    .save()
