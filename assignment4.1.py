
# coding: utf-8

# # Assignment 4
# 
# Welcome to Assignment 4. This will be the most fun. Now we will prepare data for plotting.
# 
# Just make sure you hit the play button on each cell from top to down. There are three functions you have to implement. Please also make sure than on each change on a function you hit the play button again on the corresponding cell to make it available to the rest of this notebook. Please also make sure to only implement the function bodies and DON'T add any additional code outside functions since this might confuse the autograder.
# 
# So the function below is used to make it easy for you to create a data frame from a cloudant data frame using the so called "DataSource" which is some sort of a plugin which allows ApacheSpark to use different data sources.
# 

# In[137]:

#Please don't modify this function
def readDataFrameFromCloudant(host,user,pw,database):
    cloudantdata=spark.read.format("com.cloudant.spark").     option("cloudant.host",host).     option("cloudant.username", user).     option("cloudant.password", pw).     load(database)

    cloudantdata.createOrReplaceTempView("washing")
    spark.sql("SELECT * from washing").show()
    return cloudantdata


# Sampling is one of the most important things when it comes to visualization because often the data set get so huge that you simply
# 
# - can't copy all data to a local Spark driver (Data Science Experience is using a "local" Spark driver)
# - can't throw all data at the plotting library
# 
# Please implement a function which returns a 10% sample of a given data frame:

# In[141]:

def getSample(df,spark):
    df.createOrReplaceTempView("washing")
    result = spark.sql("select * from washing where flowrate is not null and fluidlevel is not null and frequency is not null and hardness is not null and speed is not null and temperature is not null")
    result_array = result.map(lambda row : (row.flowrate, row.fluidlevel, row.frequency, row.hardness, row.speed, row.temperature).sample(False,0.1)
    return result_array


# Now we want to create a histogram and boxplot. Please ignore the sampling for now and retur a python list containing all temperature values from the data set

# In[142]:

def getListForHistogramAndBoxPlot(df,spark):
    result = spark.sql("SELECT flowrate, fluidlevel, frequency, hardness, speed, temperature from washing where flowrate is not null and fluidlevel is not null and frequency is not null and hardness is not null and speed is not null and temperature is not null")
    resultfinal_rdd = result.df.sample(False,0.1).map(lambda row : (row.flowrate, row.fluidlevel, row.frequency, row.hardness, row.speed, row.temperature)).collect()
    return df.resultfinal_rdd


# Finally we want to create a run chart. Please return two lists (encapusalted in a python tuple object) containing temperature and timestamp (ts) ordered by timestamp. Please refere to the following link to learn more about tuples in python: https://www.tutorialspoint.com/python/python_tuples.htm

# In[8]:

#should return a tuple containing the two lists for timestamp and temperature
#please make sure you take only 10% of the data by sampling
#please also ensure that you sample in a way that the timestamp samples and temperature samples correspond (=> call sample on an object still containing both dimensions)
def getListsForRunChart(df,spark):
    return #YOUR CODE GOES HERE


# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED
# #axx
# ### PLEASE DON'T REMOVE THIS BLOCK - THE FOLLOWING CODE IS NOT GRADED

# In[69]:

#TODO Please provide your Cloudant credentials here
hostname = "5770985f-edce-42f2-92f8-aa6dd1a5af41-bluemix.cloudant.com"
user = "5770985f-edce-42f2-92f8-aa6dd1a5af41-bluemix"
pw = "5d930c63ad7835e4625c99011bfa04b41789d5db917e94c2134a862f3f117061"
database = "washing"
cloudantdata=readDataFrameFromCloudant(hostname, user, pw, database)


# In[121]:

def getSample(cloudantdata,spark):
    result = spark.sql("select * from washing where flowrate is not null and fluidlevel is not null and frequency is not null and hardness is not null and speed is not null and temperature is not null")
    result_array = result.rdd.map(lambda row : row.voltage).sample(False,0.1)
    getsample= cloudantdata.result_array
    return getsample


# In[55]:

get_ipython().magic(u'matplotlib inline')
import matplotlib.pyplot as plt


# In[11]:

plt.hist(getListForHistogramAndBoxPlot(cloudantdata,spark))
plt.show()


# In[12]:

plt.boxplot(getListForHistogramAndBoxPlot(cloudantdata,spark))
plt.show()


# In[13]:

lists = getListsForRunChart(cloudantdata,spark)


# In[14]:

plt.plot(lists[0],lists[1])
plt.xlabel("time")
plt.ylabel("temperature")
plt.show()


# Congratulations, you are done! Please download the notebook as python file, name it assignment4.1.py and sumbit it to the grader.
