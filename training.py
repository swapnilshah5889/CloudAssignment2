from pyspark.sql.functions import col, isnan
from pyspark.sql import SparkSession
from pyspark.ml.feature import VectorAssembler, StandardScaler
from pyspark.ml.classification import LogisticRegression
from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidator, ParamGridBuilder
from pyspark.ml import Pipeline

def get_spark_object():
    # Get Spark instance
    spark = SparkSession.builder\
        .master("local")\
        .appName("Wine Quality Predictions")\
        .config("spark.jars.packages", "org.apache.hadoop:hadoop-aws:3.0.0")\
        .getOrCreate()

    # Configure Spark instance
    spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider",
                                                      "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")

    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key", "ASIA2XHXJ5PROEDCSK3P")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key", "FRBChR0JNkUcVVmhv1U0qzMtqI1jkN4sikrsdnJV")
    spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")
    return spark;

def read_data(spark):
    # Read CSV data
    df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "true")\
        .option("sep", ";")\
        .load("TrainingDataset.csv")

    # Loading validation data
    validation_df = spark.read.format("csv")\
        .option("header", "true")\
        .option("inferSchema", "true")\
        .option("sep", ";")\
        .load("ValidationDataset.csv")

    return [df, validation_df]

# Train model
def train_model(df, validation_df, spark):
    
    if df.count() > 0 and validation_df.count() > 0:
        print("Data loaded successfully")
    else:
        print("Something unexpected happened during data load")

    # Format columns names
    new_column_names = {
        '"""""fixed acidity""""': 'fixed_acidity',
        '"""fixed acidity""""': 'fixed_acidity',
        '""""volatile acidity""""': 'volatile_acidity',
        '""""citric acid""""': 'citric_acid',
        '""""residual sugar""""': 'residual_sugar',
        '""""chlorides""""': 'chlorides',
        '""""free sulfur dioxide""""': 'free_sulfur_dioxide',
        '""""total sulfur dioxide""""': 'total_sulfur_dioxide',
        '""""density""""': 'density',
        '""""pH""""': 'pH',
        '""""sulphates""""': 'sulphates',
        '""""alcohol""""': 'alcohol',
        '""""quality"""""': 'label'
    }

    for current_name, new_name in new_column_names.items():
        df = df.withColumnRenamed(current_name, new_name)
        validation_df = validation_df.withColumnRenamed(current_name, new_name)

    null_counts = []

    # Clean data - remove null data
    for col_name in df.columns:
        null_count = df.filter(col(col_name).isNull() | isnan(col(col_name))).count()
        null_counts.append((col_name, null_count))

    for col_name, null_count in null_counts:
        print(f"Column '{col_name}' has {null_count} null or NaN values.")

    # 70/30 split of training data
    df, test_df = df.randomSplit([0.7, 0.3], seed=42)

    assembler = VectorAssembler(
        inputCols=['fixed_acidity', 'volatile_acidity', 'citric_acid', 'residual_sugar', 'chlorides',
                   'free_sulfur_dioxide', 'total_sulfur_dioxide', 'density', 'pH', 'sulphates', 'alcohol'],
        outputCol="inputFeatures")

    scaler = StandardScaler(inputCol="inputFeatures", outputCol="features")

    # Initialize logistic regression model for training
    lr = LogisticRegression()
    pipeline1 = Pipeline(stages=[assembler, scaler, lr])
    paramgrid = ParamGridBuilder().build()
    evaluator = MulticlassClassificationEvaluator(metricName="f1")
    crossval = CrossValidator(estimator=pipeline1,
                              estimatorParamMaps=paramgrid,
                              evaluator=evaluator,
                              numFolds=10
                              )

    cvModel1 = crossval.fit(df)
    print("F1 Score for LogisticRegression Model: ", evaluator.evaluate(cvModel1.transform(test_df)))

    # Save the model to S3 bucket
    model_path = "LogisticRegression"
    cvModel1.write().overwrite().save(model_path)

if __name__ == "__main__":
    # Build and fetch the Spark object
    spark = get_spark_object()

    # Load the CSV data
    df, validation_df = read_data(spark)

    # Train the model
    train_model(df, validation_df, spark)

    # Stop the Spark instance
    spark.stop()
