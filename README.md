# Testing End-to-End AI Platform Workflow in GCP

Testing using GCP AI platform for entire modeling process - Initial 
testing/development of model to real time model predictions. 

This documentation is based on the current state of AI Platform as of 
April 2020. Note that as of this date, some aspects of AI Platform are still in
Beta, such as Custom Prediction routines. Recent updates do include Python 3.7 
and consistent runtime versions across the services.  

## Table of Contents
[AI Platform Notebooks: Development/Testing](#ai-platform-notebooks-developmenttesting)
  * [Jupyter Lab in AI Platform](#jupyter-lab-in-ai-platform)
    + [Environment variables in AI Platform Notebook](#environment-variables-in-ai-platform-notebook)
    + [Results Summary: AI Platform Notebooks/Jupyter Lab](#results-summary-ai-platform-notebooksjupyter-lab)
  * [Remote execution in AI Platform Notebook Instances](#remote-execution-in-ai-platform-notebook-instances)
    + [Remote execution: Jupyter Notebooks](#remote-execution-jupyter-notebooks)
    + [Remote Execution: Cauldron Notebooks](#remote-execution-cauldron-notebooks)
    + [Remote Execution: PyCharm IDE](#remote-execution-pycharm-ide)

[Training Jobs in AI Platform](#training-jobs-in-ai-platform)
  * [Simple training job using Jobs in AI Platform](#simple-training-job-using-jobs-in-ai-platform)
    + [Running the job locally](#running-the-job-locally)
    + [Results summary for running job locally](#results-summary-for-running-job-locally)
    + [Submit Training job to run in AI Platform](#submit-training-job-to-run-in-ai-platform)
      - [Tests and Findings for Running Job on AI Platform](#tests-and-findings-running-job-on-ai-platform)
    + [Results Summary: Running AI Platform Jobs](#results-summary-running-ai-platform-jobs)

[Model training and batch prediction using Jobs in AI Platform](#model-training-and-batch-prediction-using-jobs-in-ai-platform)
   * [Running the batch job locally](#running-the-batch-job-locally)
   * [Command for local training batch job](#command-for-local-training-batch-job)
   * [Results summary for running batch job locally](#results-summary-for-running-batch-job-locally)
   * [Submit training batch job to run in AI Platform](#submit-training-batch-job-to-run-in-ai-platform)
   * [Command to run batch job on AI Platform](#command-to-run-batch-job-on-ai-platform)
   * [Results summary for running batch job on AI Platform](#results-summary-for-running-batch-job-on-ai-platform)

[Model Deployment in AI Platform](#model-deployment-in-ai-platform)
  * [Testing with local predictions](#testing-with-local-predictions)
  * [Creation of predict package](#creation-of-predict-package)
  * [Add model prediction package to model as a version](#add-model-prediction-package-to-model-as-a-version)
  * [Get a model prediction](#get-a-model-prediction)

## AI Platform Notebooks: Development/Testing

### Jupyter Lab in AI Platform
Created a basic forecasting project using the public Iowa Liquor Sales dataset. 
See model_train_save_test.ipynb for the Jupyter Notebook. 

Includes code for pulling the data via Big Query, doing basic EDA and data 
manipulation and a basic a Random Forest Regression predicting liquor sales 
using the publicly available Iowa Liquor Sales dataset. Model quality has not 
been assessed as the code and documentation included here is focused on testing 
AI Platform services and workflows, rather than creating a usable model.

#### Environment variables in AI Platform Notebook 
In some cases you will want variables that you do not want in your 
code/committed to git. For example, bucket names, project names, or other bits 
that your org may prefer to not be in your code. The easiest way to do this is 
put the info in a file that is not tracked in git and get the info from that 
file as needed. This is appropriate for info you are fine having available to 
others you are working with, but don't want explicitly in your code. Do not 
use this for passwords. 

**Example:** Create BUCKET_NAME variable
While in the top folder of your AI Platform Notebook (above folder for repo) 
run the following command to create text file that contains the name of your 
bucket:
```
echo <bucket_name> > bucket.txt
```

In your notebook code, create a variable with your bucket name:
```
import os

bucket_path = os.path.expanduser('~/bucket.txt')
with open(bucket_path) as f:
    BUCKET_NAME = f.read().strip()
```

#### Results Summary: AI Platform Notebooks/Jupyter Lab
Coding and running the model in Jupyter Lab was uneventful. The Jupyter 
notebook in this repo should meet the needs of basic documentation. The Jupyter
notebook has now been updated to use Python 3.7 after the most recent AI 
Platform update. 

### Remote execution in AI Platform Notebook Instances

#### Remote execution: Jupyter Notebooks
Prerequisites: 
1. You must have Python 3.5+ with Jupyter installed 
2. If using a windows machine, you must have PuTTY installed. 
   If using a Mac, you should have a built-in SSH client, so PuTTY is not 
   needed.
3. You must have Cloud SDK installed: https://cloud.google.com/sdk/install

Helpful Links: 
https://cloud.google.com/ai-platform/notebooks/docs/ssh-access

Instructions:
1. Start your AI Platform Notebook Instance

2. In your command line tool of choice, run the following command to SSH into 
   your notebook instance: 

    ```
    gcloud compute ssh <instance-name>
      --project <project-name>
      --zone <zone> 
      -- 
      -L 8888:localhost:8888
    ```

    Note that the default port for Jupyter Notebook is 8888
    
3. Once you run the gcloud command, a PuTTY instance will launch and will 
   connect to your AI Platform Notebook instance. Launch Jupyter by entering 
   "jupyter-notebook" in your PuTTY instance. 

4. Copy the token shown in your PuTTY instance. 

5. Enter http://127.0.0.1:8888/ in your browser and paste the token 
   you copied in step #4

Congratulations- You are up and running!

#### Remote Execution: Cauldron Notebooks
Prerequisites:                                                             
1. You must have Python 3.6+ with cauldron-notebook python package installed on 
   your machine                      
2. If using a windows machine, you must have PuTTY installed.              
   If using a Mac, you should have a built-in SSH client, so PuTTY is not  
   needed.                                                                 
3. You must have Cloud SDK installed: https://cloud.google.com/sdk/install, 
   **including the beta packages**
                                                                           
Helpful Links:                                                             
https://cloud.google.com/ai-platform/notebooks/docs/ssh-access             
                                                                           
Instructions:  
1. Start your AI Platform Notebook Instance

2. In your command line tool of choice, run the following command to SSH into 
   your notebook instance: 
    ```
    gcloud compute ssh <instance-name>
      --project <project-id>
      --zone <zone>
      -- 
      -L 5010:localhost:5010 
    ```

3. You will now have a PuTTY window open. From here you are running commands 
   that will execute in your AI Platform Notebook instance. Note that the 
   default python version 2.7. To run anything with python 3, you need to 
   specify that. For example, using python3 or pip3. 
   
4. If you haven't already, install cauldron-notebook:
    ```
    pip3 install cauldron-notebook
    ```

5. Start Cauldron Kernel in PuTTY instance with the following command:
    ```
    cauldron kernel --port=5010
    ```

6. In your command line tool of choice, launch cauldron on your machine 
   connecting to that now open port:
    ```
    cauldron ui --connect=127.0.0.1:5010
    ```

7. Cauldron will now open in your default browser and you are ready to go!

#### Remote execution: PyCharm IDE
Prerequisites: 
1. You must have Python 3.5+ installed
2. You must have PyCharm installed with a PyCharm Professional Edition license 
3. If using a windows machine, you must have PuTTY installed. If using a Mac, 
   you should have a built-in SSH client, so PuTTY is not needed.

Helpful Links: 
    - Managing SSH keys in metadata:
    https://cloud.google.com/compute/docs/instances/adding-removing-ssh-keys
    - Creating a Remote Server Configuration in PyCharm:
    https://www.jetbrains.com/help/pycharm/creating-a-remote-server-configuration.html


Instructions:
1. On the AI Platform Notebook Instance you created, open your VM Instance 
   details. On the dropdown for Remote access, select "SSH". A linux terminal 
   will pop-up in a new window.

2. Follow the steps in the Managing SSH keys in metadata link above for 
   creating a new SSH key.

    Example:
    - In the terminal, use the ssh-keygen command to generate a private SSH key 
       file and a matching public SSH key file:
        ```
        ssh-keygen -t rsa -f ~/.ssh/<KEY_FILENAME> -C <USERNAME>
        ```
    - You will have the option here to create a passphrase as an additional 
      layer of security
    - Restrict access to your private key so that only you can read it and 
      nobody can write to it:
        ```
        chmod 400 ~/.ssh/<KEY_FILENAME>
        ```

3. Follow the steps in the Managing SSH keys in metadata link above for 
   locating an SSH key.

    Locate and save your private key:
    - In the terminal, locate your private key:
        ```
        cd /home/<USERNAME>/.ssh
        ```
    - Click on the settings in your terminal and select "Download File"
    - Enter the filepath to your private key and select "Download":
        ```
        /home/<USERNAME>/.ssh/<KEY_FILENAME>
        ```

    - Save your private key to your chosen destination
    - IMPORTANT TIP: For windows, you will need to open PuTTYgen and load your
      private key that you saved in the previous step. In PuTTYgen, select 
      "save private key" to your chosen destination. Be sure to enter your 
      passphrase if you opted to create one. This process converts your private 
      key into the format PuTTY and other third-party tools needs to be able to 
      read it.

4. Locate, view, save your public key:
    - Enter the filepath to your public key
    ```
    cd /home/<USERNAME>/.ssh
    ```
    - View and copy the entirety of the public key
    ```
    cat <KEY_FILENAME>.pub
    ```
    - Navigate to your AI Platform Instance and select "Edit"
    - Scroll to find SSH keys and select "Show and Edit"
    - Select "Add Item" and paste your public key in the box shown
    - Scroll down the page and select "Save"
        + Ensure that the key was saved properly. It should show your name and 
one key. If you are seeing multiple keys, try copying the key into a text 
editor and copying again into the VM Console.

5. Use your private key to connect PyCharm to your AI Platform Notebook 
   instance
    - Open PyCharm Professional Edition and navigate to "File" --> "Settings" 
      --> "Deployment"
    - Select "+" and "SFTP"
    - Enter your Instance External IP in the Host Section
    - IMPORTANT TIP: Your Instance External IP might be ephemeral, so you may 
      have to enter a new External IP each time you connect with PyCharm
    - Enter your username in the User Name section
    - Select authentication type as "Key Pair OpenSSH or PuTTY"
    - Upload your private key in the private key path
    - Enter your passphrase if you saved your private key with one
    - Select "Test Connection" to make sure you are connected 
    - Select "Ok"

6. You are now connected! 

To browse the files you may have saved in 
your AI Platform Notebook Instance in PyCharm, navigate to
"Tools" --> "Deployment" --> "Browse Remote Host"

The file directory of your instance should appear on the right side of your 
screen

## Training Jobs in AI Platform 

### Simple training job using Jobs in AI Platform
For the purpose of testing Jobs in AI Platform I created code for running a 
Sklearn Random Forest Regression, creating the model objects, and saving them
out to a bucket. Below is documentation for that process, as well as 
issues/gotchas found along the way. 

Helpful Links:
https://cloud.google.com/ml-engine/docs/training-jobs
https://cloud.google.com/ml-engine/docs/packaging-trainer

#### Running the job locally
It is best practice to test training your job locally (usually on a sample of 
data) to ensure your packaged code is working before submitting your job to run 
on AI Platform. Make sure to run this from the location of your repo. The 
command structure for this is:

##### Authentication:
When running locally, make sure that you are first authenticated. 

Google recommends setting up a GOOGLE_APPLICATION_CREDENTIALS path. See 
instructions here: 
https://cloud.google.com/docs/authentication/getting-started

But for those that don't want a credentials file living on their machine or 
don't have a better approach for handling that, the following gcloud command 
can be used (our recommended approach):
```
gcloud auth application-default login 
```

Base on our testing, the authentication may last for differing amounts of time 
depending on what you are doing. 

##### Command for local training job:
**Note:** See deploy.py code for a python script that simplifies the process of 
running the gcloud commands for deploying jobs and prediction routines. See the 
local_action for running local training job. If using this you can simply run 
`python deploy.py local_train` rather than the approach below.

Locations reflect structure in this repo, update for your use as appropriate. 
In this case the model output will get saved to the main directory/repo folder.

Passing in user args for bucket and run location. Adding the bucket env allows 
keeping that info out of the code and the run location allows having the code 
run differently depending on if doing this local job or running in AI Platform. 

Make sure you cd into the appropriate folder on your machine for this to run. 
In this case I'm running this from end-to-end-model-test-gcp directory.

Anything after the line that just has -- are user arguments required in the 
python code specific to the model.py code in the trainer for this repo. In 
order to make the training code work for both local training and submitting to 
AI Platform, we need to have the user defined bucket parameter here, but it can 
be set to None when running locally.

``` 
gcloud ai-platform local train  
  --package-path modeling.trainer 
  --module-name modeling.trainer.model
  --job-dir local-training-output
  --
  --run_location=local
  --bucket=None
```
 
#### Results summary for running job locally
This code ran as expected locally
 
#### Submit Training job to run in AI Platform
After testing the job locally, you are ready to create a Job on AI Platform. 
Make sure to adjust the query in the model.py to pull the right amount of 
records and that you are using the client code that is not dependent on the 
local credentials file.
  
##### Command to run Job on AI Platform (final version after testing):
First, make sure you are running in the correct project if you have multiple:
```
gcloud config set project <project-id>
```

**Note:** See deploy.py code for a python script that simplifies the process of  
running the gcloud commands for deploying jobs and prediction routines. 

**Sample running via deploy.py:**
```
python deploy.py train 
  --bucket <bucket_name_for_model_objects>
  --path <path_in_bucket_for_model_objects> 
  --name <name_of_training_job>
```

**Running directly via gcloud command:**

Locations reflect structure in this repo, update for your use as 
appropriate. 
```
gcloud ai-platform jobs submit training <job_name> 
  --package-path modeling
  --module-name modeling.trainer.model 
  --staging-bucket gs://<staging_storage_bucket_path>
  --python-version 3.7 
  --runtime-version 1.15
  --
  --bucket=<bucket_name>
```

##### Tests and Findings Running Job on AI Platform
**Test 1:** In this test I attempted to use gcloud to upload and package the 
code - this method does not require creating a setup.py and is the recommended 
method (see first method described here: 
https://cloud.google.com/ml-engine/docs/packaging-trainer). 
    
**Results:** Resulted in errors because this method did not package up the 
modules in the repo with the trainer code. In this repo, this is referring to 
the dat_prep and model_train modules. Attempted multiple tests, including 
putting these modules in different locations and deeply exploring the google 
documentation for a way to indicate we want these modules to be included. 
No solution was available. When creating the package yourself you can include 
`packages=find_packages()` so that internal packages are included, but there 
appears to be no way to specify this when using the gcloud submit training job 
command. This test was ran in Jan 2020 so it is possible this has been 
addressed, but we have not found info about that. Will re-test to confirm 
when adding additional functionality.  

**Test 2:** Create setup.py to provide instructions on what should be packaged 
with the model trainer code. Using this method we were able to specify 
`packages=find_packages()` to include our internal packages into the packaged 
code. 

**Results:** This test correctly included the modules as expected and job was 
successful

##### Results Summary: Running AI Platform Jobs
If needing to include any additional code/modules along with your code other 
than the basic model script, need to create your own setup.py rather than 
having Google do that for you. Will reach out to Google Rep about possibility 
of having an option in the gcloud tool to specify that the setuptools 
find_packages() should be include in setup.py.

General note - make sure to be thoughtful in where to save model objects to. 
Likely want some automation to this process. 

## Model training and batch prediction using Jobs in AI Platform
This section is an extension of the Training Jobs in AI Platform section. 
All of the instructions explained in that section, like setting credentials, 
should still be done before running the commands in this section. The code runs 
a Sklearn Random Forest Regression, but also trains the data by splitting the 
data into a train and test dataset. The results of the model prediction are 
saved in a BigQuery table. 

#### Running the batch job locally
It is a best practice to test a job locally. Make sure to run this from the 
location of the repo. 

##### Command for local training batch job
Since the results are being saved to BigQuery, the project needs to be 
specified along with the dataset and table in this format: dataset.table
```
gcloud ai-platform local train
  --package-path modeling.trainer
  --module-name modeling.trainer.batch_model 
  --job-dir local-training-output
  --
  --run_location=local
  --bucket=None
  --project=<project_name>
  --dataset_table=<dataset.table> 
```

The deploy.py script simplifies the process of running the gcloud commands. 
```
python deploy.py local_batch_train 
  --project=<project_name> 
  --dataset_table=<dataset.table>
```

##### Results summary for running batch job locally 
This code ran as expected locally. 

#### Submit training batch job to run in AI Platform 
After testing the job locally, you are ready to create a Job on AI Platform. 
Make sure to adjust the query in the batch_model.py to pull the right amount of
records and that you are using the client code that is not dependent on the 
local credentials file.

##### Command to run batch job on AI Platform 
Since the results are being saved to BigQuery, the project needs to be 
specified along with the dataset and table in this format: dataset.table

```
gcloud ai-platform jobs submit training <job_name> 
  --package-path modeling
  --module-name modeling.trainer.batch_model 
  --staging-bucket gs://<staging_storage_bucket_path>
  --python-version 3.7 
  --runtime-version 1.15
  --
  --bucket=<bucket_name>
  --project=<project_name>
  --dataset_table=<dataset.table>
```

The deploy.py script simplifies the process of running the gcloud commands. 
```
python deploy.py batch_train 
  --name <job_name> 
  --bucket=<bucket_name> 
  --project=<project_name> 
  --dataset_table=<dataset.table>
```

##### Results summary for running batch job on AI Platform 
This code ran as expected and finished successfully. 

## Model Development Using Training Jobs in AI Platform
**Coming Soon:** Using Training jobs during model development for testing model 
versions, including hyperparamater tuning and measuring model quality when 
training. 

## Model Deployment in AI Platform
Deploying your model for getting live model predictions!

Helpful Links:
https://cloud.google.com/ml-engine/docs/deploying-models
https://cloud.google.com/ml-engine/docs/custom-prediction-routines

If you have ran the AI Platform training job in this repo, your model object 
and supporting files are already in a bucket and ready for deployment. 

For simplicity and not duplicating code, I recommend having one package for 
model training jobs and model deployment. The code structure in this repo 
allows that and as a result allows using modules across both (reusable code) 
and only requires a single setup.py. 

### Testing with local predictions
Unfortuantely, at this time you cannot test locally if using custom prediction 
routines. For now we will skip documentation for testing locally. 

### Creation of predict package
As part of setting up your prediction package, you must create a Predictor 
class implements the instance shown under the Create Your Predictor section 
here:

https://cloud.google.com/ml-engine/docs/custom-prediction-routines

It is very important to closely follow the formatting of this as AI Platform 
strictly expects this format. The predictor module in this repo shows an 
example of working code. 

After creating the predictor code, package it and then store it in GCS. Note 
that Google recommends using a designated staging directory if iterating and 
creating multiple versions of the custom prediction routine and version can be 
used in the setup.py for this. This is setup within the setup.py in this repo.

#### Command to package up code:
```
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

### Add model prediction package to model as a version

#### Command for submitting model version
**Note:** See deploy.py code for a python script that simplifies the process of  
running the gcloud commands for deploying jobs and prediction routines.

```
gcloud beta ai-platform versions create <version>
    --model <model_name>
    --runtime-version 1.15
    --python-version 3.7
    --origin gs://<path_to_model_artifacts>
    --package-uris gs://<path_to_packaged_cd>/<name_of_package.tar.gz>
    --prediction-class <modeling.preditor.predictor.Predictor>
```

Example using deploy.py to run the above:
```
python deploy.py predict 
  --version <version_to_create>
  --model <name_of_model>
  --origin gs://<path_to_model_artifacts>
  --package-path gs://<path_to_packaged_cd>/<name_of_package.tar.gz>
```

Ran into a runtime version error - 2.1 is not yet supported. I'm not sure if 
this is just for custom prediction routines or all model deployments. Reverting
the runtime versions for training to 1.15 as a result. 

Helpful note from Google (make sure to do this to avoid overwriting files):
When you create subsequent versions of your model, organize them by placing 
each one into its own separate directory within your Cloud Storage bucket.

### Get a model prediction

#### Get a test prediction from withing the GCP Console:
1. Within the GCP Console go to AI Platform Models
2. Click on the name of the model you created
3. Click on the name of the version you created
4. Go to "Test & Use"
5. Test a model input - See sample input in the tet_prediction.json file that 
   should work if using the code in this repo. 
   
#### Python script for calling the model and getting predictions:
The predict.py file includes code that will call your model and return a 
prediction. The test_prediction.json file includes test input parameters for 
getting a sample model prediction.  

Run the following with the appropriate parameters set to get a prediction from 
your deployed model: 

**NOTE:** Make sure you are authenticated first. See training jobs section for 
more info.

```
python predict.py 
  --project <project-name>
  --model <model-name>
  --version <model-version>
```
