# Testing End-to-End AI Platform Workflow in GCP

Testing using GCP AI platform for entire modeling process - Initial 
testing/development of model to real time model predictions. 

This documentation is based on the current state of AI Platform as of early 
Jan 2020. Note that as of this date, much of AI Platform, including Notebooks
and Jobs is in Beta. AI Platform Notebooks is running version 1.14 of AI 
Platform but AI Platform Jobs provides the option of running different versions, 
including the newer 1.15 version. 1.15 includes Python 3.7, with 1.14 only 
including 1.14. 

## Creating model code in AI Platform Notebooks: Development/Testing

### Jupyter Lab in AI Platform
Created a basic forecasting project using the public Iowa Liquor Sales dataset. 
See forecasting_training_test.ipynb for the Jupyter Notebook. 

Created code for pulling the data via Big Query, doing basic EDA and data 
manipulation in order to make running a Random Forest Regression predicting 
liquor sales possible. Model quality has not been assessed as this test is for 
testing workflow rather than creating a usable model.

Coding and running the model in Jupyter Lab was uneventful. Notebook in this 
repo should meet the needs of basic documentation. Note that because AI Platform
Notebooks uses AI Platform version 1.14, we had to code in Python 3.5 (no 
f-strings or type hinting)

### Jupyter via remote execution into AI Platform Notebook Instance
Coming Soon - Some documentation already complete by team

### Cauldron via remote execution into AI Platform Notebook Instance
Coming Soon - Our team at GMI uses Cauldron Notebooks in addition to Juptyer. 

## Jobs in AI Platform 

## Simple training job using Jobs in AI Platform
For the purpose of testing Jobs in AI Platform I created code for running a 
Sklearn Random Forest Regression, creating the model objects, and saving them
out to a bucket. Below is documentation for that process, as well as 
issues/gotchas I found along the way. 

It is best practice to test training your job locally (usually on a sample of 
data) to ensure your packaged code is working before submitting your job to run 
on AI Platform. Make sure to run this from the location of your repo. The 
command structure for this is:

###### Command for local training job:
``` 
gcloud ai-platform local train  
  --package-path trainer  
  --module-name trainer.model 
  --job-dir local-training-output
```
 
 Note that there are a few lines in the model.py that you need to toggle/change 
 when running locally vs the job on AI Platform. When running locally you need 
 to point to your credentials file and should adjust the query to pull fewer 
 records. 
 
##### Results summary for running job locally
 This code ran as expected locally
 
 After testing the job locally, you are ready to create a Job on AI Platform. 
 Make sure to adjust the query in the model.py to pull the right amount of 
 records and that you are using the client code that is not dependent on the 
 local credentials file.
  
###### Command to run Job on AI Platform (final version after testing):
```
gcloud ai-platform jobs submit training test_job 
  --package-path trainer
  --module-name trainer.model 
  --staging-bucket gs://python-testing-re  
  --python-version 3.7 
  --runtime-version 1.15
```

##### Tests and Results for Running Job on AI Platform
**Test 1:** Run code as is using runtime-version 1.14 and Python 3.5 to match 
what is ran in AI Platform Notebooks. In this test I attempted to use gcloud to 
upload and package the code - this method does not require creating a setup.py 
and is the recommended method (see first method described here: 
https://cloud.google.com/ml-engine/docs/packaging-trainer). 
    
**Results:** Resulted in errors because this method did not package up the 
modules in the repo with the trainer code. In this repo, this is referring to 
the dat_prep and model_train modules. Attempted multiple tests, including 
putting these modules in different locations and deeply exploring the google 
documentation for a way to indicate we want these modules to be included. 
No solution was available. Interestingly, there is a `packages=find_packages()`
option when creating your own setup.py, but no way to specify this when using 
the gcloud command. Will bring this up with Google Rep as a recommended add. 

**Test 2:** Create setup.py to provide instructions on what should be packaged 
with the model trainer code. Using this method we were able to specify 
`packages=find_packages()` to include modules in the repo. 

**Results:** This test correctly included the modules as expected, but now that 
this problem is solve I ran into issues with the Big Query Python package that 
comes pre-installed from Google. At one point, GCP had a general google-cloud 
Python package that handled all GCP related connectivity. This is the package 
version that is included when specifying runtime version 1.14 in AI Platform 
Jobs. However,at some point Google split it out in to separate packages, such as 
google-cloud-bigquery and that is what is used in AI Platform Notebooks (also 
version 1.14). One of the changes that happened in the bigquery module is the 
ability to write .to_dataframe (`df = query_job.to_dataframe()`) on the output 
of a query job to turn it into a pandas dataframe. As a result, the version of 
google-cloud in AI Platform Jobs was not working with our current code even 
though it did work in AI Platform Notebooks. 

**Test 3:** Specify/pin google-cloud-biquery and google-cloud-storage in 
required packages within the setup.py to hopefully solve package version 
discrepancies between AI Platform Runtime 1.14 in Jobs vs Notebooks.

**Results:** This failed because it created conflicts with other pre-installed 
google-cloud packages. Given the amount of work that it would take to sync all 
this up for packages not used by this project, I decided to scrap trying to use 
runtime version 1.14 for AI Platform Jobs and test the job with version 1.15, 
even though Notebooks is not yet running this version. 

**Test 4:** Ran test using AI Platform runtime version 1.15 with Python 3.7.

**Results:** Successfully ran job 

##### Results summary for running AI Platform Job
If needing to include any additional code/modules along with your code other 
than the basic model script, need to create your own setup.py rather than having
Google do that for you. Will reach out to Google Rep about possibility of having 
an option in the gcloud tool to specify that the setuptools find_packages() 
should be include in setup.py.

Version issues between AI Platform Notebooks and AI Platform Jobs were noted. 
Note that AI Platform runtime version 1.14 comes with google-cloud package 
pre-installed, this same runtime for AI Platform Notebooks comes with the newer 
individual packages installed. This can create conflict when moving code from 
Notebooks to Jobs (or likely model serving). 

General note - make sure to be thoughtful in where to save model objects to. 
Team likely wants to add some automation to this process. 

## Batch jobs using Jobs in AI Platform
Coming Soon

## Model Development Using Jobs in AI Platform (including hyperparameter tuning)
A more complex job for model training. Can be used during model development. 
Includes hyperparamater tuning and measuring model quality when training. 

## Model Serving in AI Platform
Coming Soon
