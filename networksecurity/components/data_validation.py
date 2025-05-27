from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import DataIngestionArtifact , DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utils.utils import read_yaml_file , write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import sys , os 

class DataValidation:
    def __init__(self, data_ingestion_artifact:DataIngestionArtifact,
                 data_validation_config:DataValidationConfig):
        try:
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self.schema_config = read_yaml_file(SCHEMA_FILE_PATH)
        except Exception as e:
            raise NetworkSecurityException(e ,sys)
        
    @staticmethod
    def read_data(file_path)-> pd.DataFrame:
        try:
            return pd.read_csv(file_path)
        except Exception as  e:
            raise NetworkSecurityException(e,sys)
        
    def validate_cols(self , dataframe:pd.DataFrame ) -> bool:
        try:
            no_cols = len(self.schema_config)
            logging.info(f"Required number of columns = {no_cols}")
            logging.info(f"Dataframe has columns : {len(dataframe.columns)}")
            
            if len(dataframe.columns) == no_cols:
                return True 
            else:
             return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def validate_numerical_cols(self , dataframe:pd.DataFrame) -> bool:
        try:
            n_cols = self.schema_config["numerical_columns"]
            for col in n_cols:
                if col not in dataframe.columns:
                    return False
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def detect_data_drift(self , base_df , current_df , thershold = 0.05)->bool:
        try:
            status = True 
            report = {}
            for col in base_df.columns:
                d1 = base_df[col]
                d2 = current_df[col]
                is_sample_dist = ks_2samp(d1 , d2)
                if thershold <= is_sample_dist.pvalue:
                    is_found = False 
                else:
                    is_found = True
                    status = False
                
                report.update({col:{
                    "p_value":float(is_sample_dist.pvalue),
                    "drift_status":is_found
                }})
            
            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # Create directory
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path , exist_ok= True)
            write_yaml_file(file_path= drift_report_file_path , content= report)
        except Exception as e:
            raise NetworkSecurityException(e,sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        try:
            train_file_path = self.data_ingestion_artifact.train_file_path
            test_file_path = self.data_ingestion_artifact.test_file_path
            
            # Read Data from train and test
            train_dataframe = DataValidation.read_data(train_file_path)
            test_dataframe = DataValidation.read_data(test_file_path) 
            
            status = self.validate_cols(dataframe= train_dataframe)
            if not status:
                error_message = f"Train Dataframe doesn't contain all columns.\n"
            
            
            status = self.validate_cols(dataframe= test_dataframe)
            if not status:
                error_message = f"Test Dataframe doesn't contain all columns.\n"
            
            status = self.detect_data_drift(base_df=train_dataframe , current_df= test_dataframe)
            dir_path = os.path.dirname(self.data_validation_config.valid_train_file_path)
            os.makedirs(dir_path , exist_ok= True)
            
            train_dataframe.to_csv(
                self.data_validation_config.valid_train_file_path , index = False , header = True
            )
            
            test_dataframe.to_csv(
                self.data_validation_config.valid_test_file_path , index = False , header = True
            )
            
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path= self.data_ingestion_artifact.train_file_path,
                valid_test_file_path= self.data_ingestion_artifact.test_file_path,
                invalid_train_file_path= None ,
                invalid_test_file_path= None ,
                drift_report_file_path= self.data_validation_config.drift_report_file_path
            )
            return data_validation_artifact
        except Exception as e:
            raise NetworkSecurityException(e ,sys)   
