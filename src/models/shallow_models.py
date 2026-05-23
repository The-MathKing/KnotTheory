import numpy as np
from sklearn.linear_model import ElasticNet
from sklearn.svm import SVR
from sklearn.model_selection import KFold, cross_val_score

class RegularizedShallowArchitecture:
    """
    Replaces the DNN with a statistically sound shallow architecture 
    appropriate for N=274 samples and 79 features. 
    Implements Elastic-Net and Support Vector Regression with rigorous 5-fold CV.
    """
    def __init__(self):
        # ElasticNet combines L1 (Lasso) and L2 (Ridge) regularization 
        # to effectively handle high-dimensional, low-sample data.
        self.elastic_net = ElasticNet(alpha=0.1, l1_ratio=0.5, max_iter=5000)
        self.svr = SVR(kernel='rbf', C=1.0, epsilon=0.1)
        self.cv = KFold(n_splits=5, shuffle=True, random_state=42)

    def evaluate_pipeline(self, X, y):
        print("Executing strict 5-fold cross-validation on N=274 samples...")
        
        en_scores = cross_val_score(self.elastic_net, X, y, cv=self.cv, scoring='neg_mean_squared_error')
        svr_scores = cross_val_score(self.svr, X, y, cv=self.cv, scoring='neg_mean_squared_error')
        
        print(f"Elastic-Net CV MSE: {-np.mean(en_scores):.4f}")
        print(f"SVR CV MSE: {-np.mean(svr_scores):.4f}")
        
        return en_scores, svr_scores

if __name__ == "__main__":
    model = RegularizedShallowArchitecture()
    print("Shallow regularized pipeline initialized.")
