from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

## Configuration for the data ingestion config 

from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
import os 
import sys 
import pymongo
from typing import List
from sklearn.model_selection import train_test_split
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

MONGO_DB_URL = os.getenv("MONGO_DB_URL")

class DataIngestion:
    def __init__(self , data_ingestion_config:DataIngestionConfig):
        try:
            self.data_ingestion_config = data_ingestion_config
        except Exception as e:
            raise NetworkSecurityException(e ,sys)
        
        
    def export_collection_as_df(self):
        """
        Read data from Mongo DB
        """
        try:
            
            database_name = self.data_ingestion_config.database_name
            collection_name = self.data_ingestion_config.collection_name
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL)
            collection = self.mongo_client[database_name][collection_name]
            
            data = pd.DataFrame(list(collection.find()))
            
            if "_id" in data.columns.to_list():
                data = data.drop(columns=["_id"] , axis = 1)
                
            data.replace({"na":np.nan} , inplace=True)
            
            return data 
        
        except Exception as e:
            raise NetworkSecurityException(e ,sys)
     
    def export_data_to_feature_store(self, dataframe:pd.DataFrame):
        try:
            feature_store_file_path = self.data_ingestion_config.feature_store_file_path
            # Creating a folder 
            dir_path = os.path.dirname(feature_store_file_path)
            os.makedirs(dir_path , exist_ok= True)
            dataframe.to_csv(feature_store_file_path , index = False , header = True)
            return dataframe
        except Exception as e:
            raise NetworkSecurityException(e , sys)
        
    def split_data(self , dataframe = pd.DataFrame):
        try:
            train_set , test_set = train_test_split(
                dataframe , test_size= self.data_ingestion_config.train_test_split_ratio
            )
            logging.info("performed train test split on dataframe")
            
            dir_path = os.path.dirname(self.data_ingestion_config.training_file_path)
            
            os.makedirs(dir_path , exist_ok=True)
            
            logging.info(f"Exporting train and test file path")
            
            train_set.to_csv(
                self.data_ingestion_config.training_file_path , index = False , header = True
            )
            test_set.to_csv(
                self.data_ingestion_config.testing_file_path , index = False , header = True
            )
            
            logging.info(f"Exported train and test file path")
        except Exception as e:
            raise NetworkSecurityException(e,sys)
    
        
        
    def initiate_data_ingestion(self):
       try:
           dataframe = self.export_collection_as_df()
           data = self.export_data_to_feature_store(dataframe)
           self.split_data(data)
           data_ingestion_artifact = DataIngestionArtifact(train_file_path= self.data_ingestion_config.training_file_path,
                                                           test_file_path=  self.data_ingestion_config.testing_file_path)
           return data_ingestion_artifact
       except Exception as e:
           raise NetworkSecurityException(e , sys) 