
# coding: utf-8

# # Assignment 3
# 
# Welcome to Assignment 3. This will be even more fun. Now we will calculate statistical measures on the test data you have created.
# 
# YOU ARE NOT ALLOWED TO USE ANY OTHER 3RD PARTY LIBRARIES LIKE PANDAS. PLEASE ONLY MODIFY CONTENT INSIDE THE FUNCTION SKELETONS
# Please read why: https://www.coursera.org/learn/exploring-visualizing-iot-data/discussions/weeks/3/threads/skjCbNgeEeapeQ5W6suLkA
# . Just make sure you hit the play button on each cell from top to down. There are seven functions you have to implement. Please also make sure than on each change on a function you hit the play button again on the corresponding cell to make it available to the rest of this notebook.
# Please also make sure to only implement the function bodies and DON'T add any additional code outside functions since this might confuse the autograder.
# 
# So the function below is used to make it easy for you to create a data frame from a cloudant data frame using the so called "DataSource" which is some sort of a plugin which allows ApacheSpark to use different data sources.
# 

# In[196]:

#Please don't modify this function
def readDataFrameFromCloudant(host,user,pw,database):
    cloudantdata=spark.read.format("com.cloudant.spark").     option("cloudant.host",host).     option("cloudant.username", user).     option("cloudant.password", pw).     load(database)

    cloudantdata.createOrReplaceTempView("washing")
    spark.sql("SELECT * from washing").show()
    return cloudantdata


# All functions can be implemented using DataFrames, ApacheSparkSQL or RDDs. We are only interested in the result. You are given the reference to the data frame in the "df" parameter and in case you want to use SQL just use the "spark" parameter which is a reference to the global SparkSession object. Finally if you want to use RDDs just use "df.rdd" for obtaining a reference to the underlying RDD object. 
# 
# Let's start with the first function. Please calculate the minimal temperature for the test data set you have created. We've provided a little skeleton for you in case you want to use SQL. You can use this skeleton for all subsequent functions. Everything can be implemented using SQL only if you like.

# In[197]:

def minTemperature(df,spark):
    return spark.sql("SELECT MIN(temperature) as mintemp from washing").first().mintemp


# Please now do the same for the mean of the temperature

# In[198]:

def meanTemperature(df,spark):
    return spark.sql("SELECT AVG(temperature) as avgtemp from washing").first().avgtemp


# Please now do the same for the maximum of the temperature

# In[199]:

def maxTemperature(df,spark):
    return spark.sql("SELECT MAX(temperature) as maxtemp from washing").first().maxtemp


# Please now do the same for the standard deviation of the temperature

# In[200]:

def sdTemperature(df,spark):
    return spark.sql("SELECT STDDEV(temperature) as stddevtemp from washing").first().stddevtemp


# Please now do the same for the skew of the temperature. Since the SQL statement for this is a bit more complicated we've provided a skeleton for you. You have to insert custom code at four position in order to make the function work. Alternatively you can also remove everything and implement if on your own. Note that we are making use of two previously defined functions, so please make sure they are correct. Also note that we are making use of python's string formatting capabilitis where the results of the two function calls to "meanTemperature" and "sdTemperature" are inserted at the "%s" symbols in the SQL string.

# In[201]:

def skewTemperature(df,spark):
    return spark.sql("""SELECT (SELECT 1/COUNT(temperature) from washing)*SUM(POWER(temperature-%s,3)/POWER(%s,3))as skewness from washing where temperature is not null""" %(meanTemperature(df,spark),sdTemperature(df,spark))).first().skewness


# Kurtosis is the 4th statistical moment, so if you are smart you can make use of the code for skew which is the 3rd statistical moment. Actually only two things are different.

# In[202]:

def kurtosisTemperature(df,spark):    
    return spark.sql("""SELECT (SELECT 1/COUNT(temperature) from washing)*SUM(POWER(temperature-%s,4)/POWER(%s,4))as kurtosis from washing where temperature is not null""" %(meanTemperature(df,spark),sdTemperature(df,spark))).first().kurtosis


# Just a hint. This can be solved easily using SQL as well, but as shown in the lecture also using RDDs.

# In[267]:

def correlationTemperatureHardness(df,spark):
    return spark.sql("SELECT CORR(temperature, hardness) as correlation from washing").first().correlation


# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED
# #axx
# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED

# In[212]:

#TODO Please provide your Cloudant credentials here
hostname = "5770985f-edce-42f2-92f8-aa6dd1a5af41-bluemix.cloudant.com"
user = "5770985f-edce-42f2-92f8-aa6dd1a5af41-bluemix"
pw = "5d930c63ad7835e4625c99011bfa04b41789d5db917e94c2134a862f3f117061"
database = "washing"
cloudantdata=readDataFrameFromCloudant(hostname, user, pw, database)


# In[213]:

minTemperature(cloudantdata,spark)
mintemp=spark.sql("SELECT MIN(temperature) as mintemp from washing").first().mintemp
print(mintemp)


# In[214]:

meanTemperature(cloudantdata,spark)
avgtemp=spark.sql("SELECT AVG(temperature) as avgtemp from washing").first().avgtemp
print(avgtemp)


# In[215]:

maxTemperature(cloudantdata,spark)
maxtemp=spark.sql("SELECT MAX(temperature) as maxtemp from washing").first().maxtemp
print(maxtemp)


# In[216]:

sdTemperature(cloudantdata,spark)
stddevtemp=spark.sql("SELECT STDDEV(temperature) as stddevtemp from washing").first().stddevtemp
print(stddevtemp)


# In[217]:

skewTemperature(cloudantdata,spark)
skewness=spark.sql("""SELECT (SELECT 1/COUNT(temperature) from washing)*SUM(POWER(temperature-%s,3)/POWER(%s,3))as skewness from washing where temperature is not null""" %(meanTemperature(cloudantdata,spark),sdTemperature(cloudantdata,spark))).first().skewness
print(skewness)


# In[218]:

kurtosisTemperature(cloudantdata,spark)
kurtosis=spark.sql("""SELECT (SELECT 1/COUNT(temperature) from washing)*SUM(POWER(temperature-%s,4)/POWER(%s,4))as kurtosis from washing where temperature is not null""" %(meanTemperature(cloudantdata,spark),sdTemperature(cloudantdata,spark))).first().kurtosis
print(kurtosis)


# In[268]:

correlationTemperatureHardness(cloudantdata,spark) 
correlation=spark.sql("SELECT CORR(temperature, hardness) as correlation from washing").first().correlation
print(correlation)


# In[ ]:

#this is the manual function of correlation
def correlationTemperatureHardness(df,spark):
    htData=spark.sql("SELECT hardness, temperature FROM washing").dropna()
    htSum=htData.groupBy().sum('hardness', 'temperature').collect()
    c=htData.count()
    hSum=htSum[0][0]
    tSum=htSum[0][1]
    hMean=hSum/float(c)
    tMean=tSum/float(c)
    covData=htData.rdd.map(lambda (x,y) : (x-hMean)*(y-tMean)).sum()/c
    sdH=spark.sql("SELECT STDDEV(hardness) AS sdH FROM washing").first().sdH
    sdT=spark.sql("SELECT STDDEV(temperature) AS sdT FROM washing").first().sdT
    corrHT=covData / (sdH * sdT)
    return corrHT


# Congratulations, you are done, please download this notebook as python file using the export function and submit is to the gader using the filename "assignment3.1.py"
