from sensor.entity import artifact_entity,config_entity
from sensor.exception import CustomException
from sensor.logger import logging
from typing import Optional
import os,sys
from xgboost import XGBClassifier
from sensor import utils
import numpy as np



class ModelTrainer:
    
    def __init__(self,model_trainfer_config:config_entity.ModelTrainerConfig,
                 data_transformation_artifact:artifact_entity.DataTransformationArtifact
                 ):
        try:
            self.model_trainer_config=model_trainfer_config
            self.data_transformation_artifact=data_transformation_artifact
            
            
        except Exception as e:
            raise CustomException(e,sys)
        
    def fine_tune(self):
        try:
            # Code for Grid search CV
            pass
        
    def train_model(self,x,y):
        try:
            xgb_clf = XGBClassifier()
            xgb_clf.fit(x,y)
            return xgb_clf
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_model_trainer(self,)->artifact_entity.ModelTrainerArtifact:
        try:
            logging.info(f"Loading train and test array")
            train_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_train_path)
            test_arr = utils.load_numpy_array_data(file_path=self.data_transformation_artifact.transformed_test_path)
            
            logging.info(f"Splitting the input and target feature from both train and test arr.")
            x_train,y_train = train_arr[:,:-1],train_arr[:,-1]
            x_test,y_test = test_arr[:,:-1],test_arr[:,-1]
            
            logging.info(f"Train the model")
            model = self.train_model(x=x_train,y=y_train)
            
            logging.info(f"Calculate the f1 test score")
            yhat_train = model.predict(x_train)
            f1_train_score = f1_score(y_true=y_train,y_pred=yhat_train)
            
            logging.info(f"Calculating f1 test scoer")
            yhat_test = model.predict(x_test)
            f1_test_score = f1_score(y_true=y_test,y_pred=yhat_test)
            
            logging.info(f"train score: {f1_train_score} and tests score {f1_test_score}")
            if f1_test_score<self.model_trainer_config.expected_score:
                raise Exception(f"MOdel is not good as it's unable to produce expected accuracy: {self.model_trainer_config.expected_score}: model actual score: {f1_test_score}")
            
            logging.info(f"Checking if our model is underfitting or not")
            diff = abs(f1_train_score-f1_test_score)
            
            if diff>self.model_trainer_config.overfitting_threshold:
                raise Exception(f"Train and test score diff: {diff} is more than overfitting threshold {self.model_trainer_config.overfitting_threshold}")
            
            #Save the trained model
            logging.info(f"savinf mode object")
            utils.save_object(file_path=self.model_trainer_config.model_path,obj=model)
            
            #prepare artifact
            logging.info("Prepare the artificat")
            model_trainer_artifact = artifact_entity.ModelTrainerArtifact(model_path=self.model_trainer_config.model_path,
                                    f1_train_score=f1_train_score,f1_test_score=f1_test_score)
            
            return model_trainer_artifact
        
        except Exception as e:
            raise CustomException(e,sys)