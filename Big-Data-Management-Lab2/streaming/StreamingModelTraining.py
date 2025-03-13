from pyspark.sql import SparkSession
from pyspark.sql.functions import *
from pyspark.sql.types import *
import sys
import os
from pyspark.ml.feature import VectorAssembler
from pyspark.ml.regression import RandomForestRegressor
from pyspark.ml.tuning import ParamGridBuilder
import numpy as np
from pyspark.ml import Pipeline
from pyspark.ml.tuning import CrossValidator
from pyspark.ml.evaluation import RegressionEvaluator
import matplotlib.pyplot as plt

os.environ['PYSPARK_PYTHON'] = sys.executable
os.environ['PYSPARK_DRIVER_PYTHON'] = sys.executable


def createMongoConnexion():
    spark = SparkSession.builder.master(f"local[*]").appName("myApp")\
    .config('spark.jars.packages', 'org.mongodb.spark:mongo-spark-connector_2.12:3.0.1')\
        .getOrCreate()

    spark.sparkContext.setLogLevel("WARN")
    return spark



def dataPreparation(spark):
    #read idealista data
    idealista = spark_m.read.format("mongo")     .option('uri', 'mongodb://localhost:27017/formatted.idealista')     .load()     .cache()
    #extract training features
    rdd=idealista.rdd.map(lambda x: ((int(x['neighborhood_id_reconciled'][1:]), x['bathrooms']/x['rooms'],x['price'])))
    df=rdd.toDF()
    #rename the features
    df=df.selectExpr(
    '_1 AS neighborhood_id',
    '_2 AS label',
    '_3 AS price')
    
    return df


def modelTraining(train):
    #convert multiple features into one features vector
    assembler = VectorAssembler(
    inputCols=["neighborhood_id","price"],
    outputCol="features")
    
    #Random Forest Regressor
    rf = RandomForestRegressor(featuresCol = 'features', labelCol = 'label')
    pipeline = Pipeline(stages=[assembler, rf])
    
    #Hyperparameters tuning
    paramGrid = ParamGridBuilder().addGrid(rf.numTrees, [int(x) for x in np.linspace(start = 10, stop = 50, num = 5)])\
        .addGrid(rf.maxDepth, [int(x) for x in np.linspace(start = 5, stop = 25, num = 5)])\
            .build()
    
    crossval = CrossValidator(estimator=pipeline,
                          estimatorParamMaps=paramGrid,
                          evaluator=RegressionEvaluator(),
                          numFolds=3)
    
    cvModel = crossval.fit(train)
    
    return cvModel

if __name__ == "__main__":
    spark_m=createMongoConnexion()
    # (f"Hadoop version = {spark_m._sc._jvm.org.apache.hadoop.util.VersionInfo.getVersion()}") 

    df=dataPreparation(spark_m)
    train, test = df.randomSplit([0.7, 0.3], seed = 2018)
    print("Training Dataset Count: " + str(train.count()))
    print("Test Dataset Count: " + str(test.count()))

    cvModel=modelTraining(train)

    predictions = cvModel.transform(test)

    evaluator = RegressionEvaluator(labelCol="label", predictionCol="prediction", metricName="rmse")
    rmse = evaluator.evaluate(predictions)
    rfPred = cvModel.transform(test)
    # rfResult = rfPred.toPandas()
    # plt.plot(rfResult.label, rfResult.prediction, 'bo')
    # plt.xlabel('Price')
    # plt.ylabel('Prediction')
    # plt.suptitle("Model Performance RMSE: %f" % rmse)
    # plt.show()
    cvModel.write().overwrite().save('trained_model/modelRF')
