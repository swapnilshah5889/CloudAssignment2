from pyspark.ml.evaluation import MulticlassClassificationEvaluator
from pyspark.ml.tuning import CrossValidatorModel
from pyspark.sql.session import SparkSession

# Get Spark Model
def getSparkBuild():
  # Build and configure spark model
  spark = SparkSession.builder\
            .appName("Wine Quality Predictions")\
            .getOrCreate()
  spark.sparkContext._jsc.hadoopConfiguration().set("com.amazonaws.services.s3.enableV4", "true")
  spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.impl", "org.apache.hadoop.fs.s3a.S3AFileSystem")
  spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.aws.credentials.provider", \
                                      "com.amazonaws.auth.InstanceProfileCredentialsProvider,com.amazonaws.auth.DefaultAWSCredentialsProviderChain")
  spark.sparkContext._jsc.hadoopConfiguration().set("fs.AbstractFileSystem.s3a.impl", "org.apache.hadoop.fs.s3a.S3A")

  spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.access.key","ASIA2XHXJ5PROEDCSK3P")
  spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.secret.key","FRBChR0JNkUcVVmhv1U0qzMtqI1jkN4sikrsdnJV")
  spark.sparkContext._jsc.hadoopConfiguration().set("fs.s3a.endpoint", "s3.us-east-1.amazonaws.com")
  return spark

# Load CSV data
def loadData(spark):
  
  # Load csv data
  validation_df = spark.read.format("csv")\
                      .option("header", "true")\
                      .option("inferSchema", "true")\
                      .option("sep", ";")\
                      .load("ValidationDataset.csv")
  
  if(validation_df.count()>0):
    print("Data loaded successfully")
  else:
    print("Something unexpected happend dureing data load")

  return validation_df

# Predict model 
def predictModel(validation_df): 
  
  # Format columns
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
      validation_df = validation_df.withColumnRenamed(current_name, new_name)
  
  # Predict data using model 
  model = CrossValidatorModel.load('LogisticRegression')
  evaluator = MulticlassClassificationEvaluator(metricName="f1")
  print("F1 Score for Logistic Regression Model: ", evaluator.evaluate(model.transform(validation_df)))

# Main method
if __name__ == "__main__":

  # Get spark model
  spark = getSparkBuild()

  # Load data to predict
  validation_df = loadData(spark)
  
  # Predict wine classification using the logistic regression model
  predictModel(validation_df)
