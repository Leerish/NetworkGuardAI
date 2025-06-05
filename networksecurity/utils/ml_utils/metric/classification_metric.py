from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from sklearn.metrics import f1_score , precision_score , recall_score
import sys , os

def get_classification_score(y_true , y_pred) -> ClassificationMetricArtifact:
    try:
        f1 = f1_score(y_true , y_pred)
        recall = recall_score(y_true , y_pred)
        precision = precision_score(y_true , y_pred)
        
        classification_metric = ClassificationMetricArtifact(f1_score = f1 ,
                                                             precision_score= precision ,
                                                             recall_score= recall)
        return classification_metric
    except Exception as e:
        raise NetworkSecurityException(e ,sys)
    
