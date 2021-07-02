# CryptoAdvice API 
Le API REST est développé avec le framwork python (FastAPI).
Elle permet d'exposer les données resultat des diférents modéles du projet crypto-advice (prediction de prix, sentiment analysis des tweets, metrics de blackchain ..)

Ce projet comprends aussi un template de conterisation pour cette api, et publication de l'image dans la registry GCP du PA5. 

## Commandes
1. Run de l'api en local : 
    * `make run` 
2. Build de l'image en local (Docker):  
    * `make build` 
3. Run de l'api en local (Docker) : 
    * `make run_container`  
4. Tag image avant push :  
    * `make tag`  
5. Push image :  
    * `make push` 
6. Supprimer l'image en local (Docker) : 
    * `make clean`  
