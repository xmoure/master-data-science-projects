from pyspark.sql import SparkSession
import os
import string
from pyspark.sql.functions import col

from unidecode import unidecode
import glob
from pyspark.sql.types import *

base_path = "/Users/ximenamoure/Desktop/BDM_DATA_USED/idealista/"
idealista_dirs = [d for d in os.listdir(base_path) if os.path.isdir(base_path + "/" + d)]
idealista_dirs[:5]


spark = SparkSession \
    .builder \
    .master(f"local[*]") \
    .appName("myApp") \
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1') \
    .getOrCreate()

sc = spark.sparkContext

rent_district_rdd = spark.read.format("mongo") \
    .option('uri', f"mongodb://localhost:27017/landing.rent_lookup_district") \
    .load()\
    .rdd \
    .cache()

rent_neigh_rdd = spark.read.format("mongo") \
    .option('uri', f"mongodb://localhost:27017/landing.rent_lookup_neighborhood") \
    .load() \
    .rdd \
    .cache()

rdd_neighborhood = rent_neigh_rdd.map(lambda line: (line['ne_n'].replace(" ", ""), line))
rdd_district = rent_district_rdd.map(lambda line: (line['di_n'].replace(" ", ""), line))
print(rdd_district.first())
print(rdd_neighborhood.first())

rdd = sc.emptyRDD()
for i, idealistaDir in enumerate(idealista_dirs):
    filePath = base_path + idealistaDir
    parquetFile = glob.glob(filePath + "/" + "*.parquet")[0]
    parDF = spark.read.parquet(parquetFile)
    if ("neighborhood" not in parDF.columns):
        continue
    rdd_idealista = parDF.filter(col('neighborhood').isNotNull()).rdd
    #         rdd_idealista = parDF.rdd

    date_ext = idealistaDir.split("_")[0] + "/" + idealistaDir.split("_")[1] + "/" + idealistaDir.split("_")[2]
    try:
        rdd_idealista = rdd_idealista.map(lambda line: (unidecode(line['neighborhood'].lower().translate(
            str.maketrans('', '', string.punctuation))).replace(" ", "")
                                                        , Row(**line.asDict(), date_ext=date_ext)))

        rdd_idealista = rdd_idealista.join(rdd_neighborhood).map(lambda x: (Row(neighborhood_id_reconciled=x[1][1][0],
                                                                                neighborhood_name_reconciled=x[1][1][3],
                                                                                date_ext=x[1][0]['date_ext'],
                                                                                year=x[1][0]['date_ext'].split("/")[0],
                                                                                address=x[1][0]['address'],
                                                                                bathrooms=x[1][0]['bathrooms'],
                                                                                country=x[1][0]['country'],
                                                                                typology=x[1][0]['detailedType'][
                                                                                    'typology'],
                                                                                distance=x[1][0]['distance'],
                                                                                district=x[1][0]['district'],
                                                                                exterior=x[1][0]['exterior'],
                                                                                floor=x[1][0]['floor'],
                                                                                has360=x[1][0]['has360'],
                                                                                has3DTour=x[1][0]['has3DTour'],
                                                                                hasLift=x[1][0]['hasLift'],
                                                                                hasPlan=x[1][0]['hasPlan'],
                                                                                hasStaging=x[1][0]['hasStaging'],
                                                                                hasVideo=x[1][0]['hasVideo'],
                                                                                latitude=x[1][0]['latitude'],
                                                                                longitude=x[1][0]['longitude'],
                                                                                municipality=x[1][0]['municipality'],
                                                                                neighborhood=x[1][0]['neighborhood'],
                                                                                newDevelopment=x[1][0][
                                                                                    'newDevelopment'],
                                                                                numPhotos=x[1][0]['numPhotos'],
                                                                                operation=x[1][0]['operation'],
                                                                                price=x[1][0]['price'],
                                                                                priceByArea=x[1][0]['priceByArea'],
                                                                                propertyCode=x[1][0]['propertyCode'],
                                                                                propertyType=x[1][0]['propertyType'],
                                                                                province=x[1][0]['province'],
                                                                                rooms=x[1][0]['rooms'],
                                                                                showAddress=x[1][0]['showAddress'],
                                                                                size=x[1][0]['size'],
                                                                                status=x[1][0]['status'],
                                                                                subtitle=x[1][0]['suggestedTexts'][
                                                                                    'subtitle'],
                                                                                title=x[1][0]['suggestedTexts'][
                                                                                    'title'],
                                                                                thumbnail=x[1][0]['thumbnail'],
                                                                                topNewDevelopment=x[1][0][
                                                                                    'topNewDevelopment'],
                                                                                url=x[1][0]['url']
                                                                                )))
        rdd_idealista = rdd_idealista.map(lambda line: (unidecode(line['district'].lower().translate(
            str.maketrans('', '', string.punctuation))).replace(" ", "")
                                                        , Row(**line.asDict())))
        rdd_idealista = rdd_idealista.join(rdd_district).map(
            lambda x: (Row(district_id_reconciled=x[1][1][0], district_reconciled=x[1][1][3], **x[1][0].asDict())))
        rdd = rdd.union(rdd_idealista)
        rdd.first()
    except:
        pass


print("rdd", rdd.count())
df = rdd.toDF()

df.write \
    .format("com.mongodb.spark.sql.DefaultSource") \
    .mode("overwrite") \
    .option('uri', f"mongodb://localhost:27017/formatted.idealista") \
    .save()
