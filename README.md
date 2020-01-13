# Testing End-to-End AI Platform Workflow in GCP

Testing using GCP AI platform for entire modeling process - Initial 
testing/development of model to real time model predictions. 

## Creating model code in AI Platform Notebooks: Development/Testing

### Jupyter Lab in AI Platform
Test complete - see forecasting_training_test.ipynb

### Jupyter via remote execution into AI Platform Notebook Instance
Coming Soon - Some documentation already complete by team

### Cauldron via remote execution into AI Platform Notebook Instance
Coming Soon - Our team at GMI uses Cauldron Notebooks in addition to Juptyer. 

## Jobs in AI Platform 

## Simple training job using Jobs in AI Platform
Test packaging up code for running as a training job in AI Platform

#### Command for local training job:
``` 
gcloud ai-platform local train  
  --package-path trainer  
  --module-name trainer.model 
  --job-dir local-training-output
```
  
#### Command to run job via on AI Platform:
```
gcloud ai-platform jobs submit training test_job 
  --package-path trainer
  --module-name trainer.model 
  --staging-bucket gs://python-testing-re  
  --python-version 3.7 
  --runtime-version 1.15
```

## Batch jobs using Jobs in AI Platform
Coming Soon

## Model Development Using Jobs in AI Platform (including hyperparameter tuning)
A more complex job for model training. Can be used during model development. 
Includes hyperparamater tuning and measuring model quality when training. 

## Model Serving in AI Platform
Coming Soon
