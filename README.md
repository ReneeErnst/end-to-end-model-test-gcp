# Testing End-to-End AI Platform Workflow in GCP

Testing using GCP AI platform for entire modeling process - Initial testing/development of 
model to real time model predictions



# Command for local training job:
gcloud ai-platform local train  
  --package-path trainer  
  --module-name trainer.model 
  --job-dir local-training-output
  
# Command to run job via on AI Platform:
gcloud ai-platform jobs submit training test_job3 
  --package-path trainer/ 
  --module-name trainer.model 
  --staging-bucket gs://python-testing-re  
  --python-version 3.5 
  --runtime-version 1.14