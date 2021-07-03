# IAC Terraform 
In this project you have the infrastructure as code project that allow you to deploy all CryptoAdvice project infrastructure  

## Requerements : 
* First step is to creat service account in GCP UI with owner role of PA5-Crupto-Advice project

* Then Create keys to login terraform using this service account with below command line
	* `gcloud iam service-accounts keys create .key-file.json  --iam-account=pa5-sa@pa5-crypto-advice.iam.gserviceaccount.com`

* Set terraform variable credentials on set the GOOGLE_APPLICATION_CREDENTIALS variable envirenement that is used by terraform client 
	* `export GOOGLE_APPLICATION_CREDENTIALS=.key-file.json `

* In GCP enable Cloud Resource Manager API for the project and other API that is used like   Pub/Sub API, DataFlow API, GKE API, BigQuery API. 

## Deploy Infrastructure
* Initialize Terraform :
	* `terraform init`

* Scan Terrafoem manifests : 
	* `terraform plan`

* Run deployment : 
	* `terraform apply`