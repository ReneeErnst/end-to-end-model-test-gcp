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

#### Set Environment variables in AI Platform Notebook 
In some cases you will want variables that you do not want in your 
code/committed to git. For example, bucket names, project names, or other bits 
that your org may prefer to not be in your code. The easiest way to do this is 
put the info in a file that is not tracked in git and call it. 

**Example:** Create BUCKET_NAME variable
While in the top folder of your AI Platform Notebook (above folder for repo) run 
the following command to create text file that contains the name of your bucket:
```
echo <bucket_name> > bucket.txt
```

In your notebook code, create a variable with your bucket name:
```python
import os

bucket_path = os.path.expanduser('~/bucket.txt')
with open(bucket_path) as f:
    BUCKET_NAME = f.read().strip()
```

#### Results Summary
Coding and running the model in Jupyter Lab was uneventful. Notebook in this 
repo should meet the needs of basic documentation. Note that because AI Platform
Notebooks uses AI Platform version 1.14, we had to code in Python 3.5 (no 
f-strings or type hinting)

### Jupyter via remote execution into AI Platform Notebook Instance
Prerequisites: 
1. You must have Python 3.5+ with Jupyter installed 
2. If using a windows machine, you must have PuTTY installed. 
   If using a Mac, you should have a built-in SSH client, so PuTTY is not 
   needed.
3. You must have Cloud SDK installed: https://cloud.google.com/sdk/install

Helpful Links: 
https://cloud.google.com/ai-platform/notebooks/docs/ssh-access

Instructions:
1. On the AI Platform Notebook Instance you created,
open your VM Instance details.
On the dropdown for Remote access, select "view gcloud command"
Your Project-Id, Zone, and Instance Name all need to be in quotations.
Example: 
```
gcloud compute --project <project-id> ssh --zone <zone-name> <instance-name>
```

2. Open your local Google Cloud SDK shell and run the gcloud command
for connecting.
Tip- you will want to include a port at this time. Note that the default
port for Jupyter Notebook is 8888
Example:
```
gcloud compute --project <project-id> ssh --zone <zone-name> <instance-name>
-- -L 8888:localhost:8888
```
3. Once you run the gcloud command, a PuTTY instance will launch and
will connect to your AI Platform Notebook instance. Launch Jupyter
by entering "jupyter-notebook" in your PuTTY instance. 

4. Copy the token shown in your PuTTY instance. 

5. Enter http://127.0.0.1:8888/ in your browser and paste the token 
you copied in step #4

Congratulations- You are up and running!

### Cauldron via remote execution into AI Platform Notebook Instance
Coming Soon - Our team at GMI uses Cauldron Notebooks in addition to Juptyer. 

## Jobs in AI Platform 

### Simple training job using Jobs in AI Platform
For the purpose of testing Jobs in AI Platform I created code for running a 
Sklearn Random Forest Regression, creating the model objects, and saving them
out to a bucket. Below is documentation for that process, as well as 
issues/gotchas I found along the way. 

Helpful Links:
https://cloud.google.com/ml-engine/docs/training-jobs
https://cloud.google.com/ml-engine/docs/packaging-trainer

#### Running the job locally
It is best practice to test training your job locally (usually on a sample of 
data) to ensure your packaged code is working before submitting your job to run 
on AI Platform. Make sure to run this from the location of your repo. The 
command structure for this is:

##### Command for local training job:
**Note:** See deploy.py code for a python script that simplifies the process of  
running the gcloud commands for deploying jobs and prediction routines. 

Locations reflect structure in this repo, update for your use as 
appropriate. In this case the model output will get saved to the main 
directory/repo folder.

Passing in user args for bucket and run location. Adding the bucket env allows 
keeping that info out of the code and the run location allows having the code 
run differently depending on if doing this local job or running in AI Platform. 

``` 
gcloud ai-platform local train  
  --package-path trainer 
  --module-name trainer.model
  --job-dir local-training-output
  --
  --bucket=<bucket_name>
  --run_locatin=local
```
 
#### Results summary for running job locally
This code ran as expected locally
 
#### Submit Training job to run in AI Platform
After testing the job locally, you are ready to create a Job on AI Platform. 
Make sure to adjust the query in the model.py to pull the right amount of 
records and that you are using the client code that is not dependent on the 
local credentials file.
  
##### Command to run Job on AI Platform (final version after testing):
**Note:** See deploy.py code for a python script that simplifies the process of  
running the gcloud commands for deploying jobs and prediction routines. 

Locations reflect structure in this repo, update for your use as 
appropriate. 
```
gcloud ai-platform jobs submit training <job_name> 
  --package-path modeling
  --module-name modeling.trainer.model 
  --staging-bucket gs://<your_bucket>
  --python-version 3.7 
  --runtime-version 1.15
  --
  --bucket=<bucket_name>
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

## Model Deployment in AI Platform
Helpful Links:
https://cloud.google.com/ml-engine/docs/deploying-models
https://cloud.google.com/ml-engine/docs/custom-prediction-routines

Helpful note from Google (make sure to do this to avoid overwriting files):
When you create subsequent versions of your model, organize them by placing each
one into its own separate directory within your Cloud Storage bucket.

Note that if you used the code in this repo, your model object and supporting 
files are already in a bucket and ready for deployment. 

### Testing with local predictions
Unfortuantely, at this time you can't test locally if using custom prediction 
routines. For now we will skip documentation for testing locally. 

### Creation of predict package
As part of setting up your prediction package, you must create a Predictor class
implements the instance shown under the Create Your Predictor section here:
https://cloud.google.com/ml-engine/docs/custom-prediction-routines

It is very important to closely follow the formatting of this as AI Platform 
strictly expects this format. The predictor module in this repo shows an example
of working code. 

After creating the predictor code, package it and then store it in GCS. Note 
that Google recommends using a designated staging directory if iterating and 
creating multiple versions of the custom prediction routine and version can be 
used in the setup.py for this. This is setup within the setup.py in this repo.

#### Command to package up code:
```python
python setup.py sdist --formats=gztar
```

This will create your packaged model in a folder called dist in your repo. Now 
you need to transfer this package to GCS.

#### Command for transferring package to GCS:
```
gsutil cp dist/<package-name>.tar.gz gs://<your-bucket>/<path-to-staging-dir>/
```

#### Create location for model versions
After creating the package and transferring it to your storage bucket, you will
wan't to create a model in AI Platform Models before adding your package as a 
version. The documentation is a bit unclear on this point. Creating a model by 
itself does not then host your model. You first need to create the "model" and 
then add your package as a version. You first want to create model using the 
following command:
```
gcloud ai-platform models create <model-name> --regions <region>
```

Note: I received an odd error when first attempting this via the gcloud command
rather than the console. The error indicated that I do not have permission to 
access my project. This error is not a clear indicator of the true issue given
that I can access the project in other ways (for example listing ai platform 
jobs), and I was able to create the model via the console without issue. 

### Add model prediction package to model as a version - requires gcloud beta

#### Command for submitting model version
```
gcloud beta ai-platform versions create <version>
    --model <model_name>
    --runtime-version 1.15
    --python-version 3.7
    --origin gs://<path_to_model_artifacts>
    --package-uris gs://<path_to_packaged_cd>/<name_of_package.tar.gz>
    --prediction-class <modeling.preditor.predictor.Predictor>
```

Ran into multiple issues when doing this, the main one being that errors are 
very vague. No information is given on exactly what part of the code isn't 
working, just a general "model" error. For example, I received the following
generic error:

```
Create Version failed. Bad model detected with error:  "Failed to load model: 
Unexpected error when loading the model: Support for generic buffers has not 
been implemented. (Error code: 0)"
```

It turns out that it was unable to load hdf files even though the tables 
requirement is included in the setup.py, and that I was able to create hdf files
in AI Platform Jobs and AI Platform Notebooks. My best guess is this is 
versioning discrepancies in AI Platform (similar to my jobs issue with AI 
Platform runtime 1.14 described above). However, the lack of error information 
passed to users makes debugging exceptionally hard. Solution here was to pickle
dataframes rather than utilizing hdf files, but took a lot of guessing to find 
the eventual issue. 

### Testing AI Platform Predict
For simplicity and not duplicating code, I recommend having one package for 
model training and model deployment. The code structure in this repo allows that
and as a result only requires a single setup.py. 

#### Command to run AI Platform Prediction Deployment
**Note:** See deploy.py code for a python script that simplifies the process of  
running the gcloud commands for deploying jobs and prediction routines. 


