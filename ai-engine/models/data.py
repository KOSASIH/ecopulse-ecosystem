import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
from plotly.offline import iplot
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import roc_auc_score, f1_score, precision_score, recall_score
from sklearn.utils.class_weight import compute_class_weight
from imblearn.over_sampling import SMOTE
from imblearn.under_sampling import RandomUnderSampler
from imblearn.pipeline import Pipeline as ImbPipeline
from collections import Counter

class DataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.data = pd.read_csv(file_path)

    def preprocess_data(self):
        # Handle missing values
        self.data.fillna(self.data.mean(), inplace=True)

        # Encode categorical variables
        categorical_cols = self.data.select_dtypes(include=['object']).columns
        for col in categorical_cols:
            le = LabelEncoder()
            self.data[col] = le.fit_transform(self.data[col])

        # Scale numerical variables
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        scaler = StandardScaler()
        self.data[numerical_cols] = scaler.fit_transform(self.data[numerical_cols])

        # Feature selection
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        selector = SelectKBest(chi2, k=10)
        X_selected = selector.fit_transform(X, y)
        self.data = pd.concat((pd.DataFrame(X_selected), y), axis=1)

        return self.data

    def split_data(self, test_size=0.2, random_state=42):
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
        return X_train, X_test, y_train, y_test

    def evaluate_model(self, y_pred, y_test):
        accuracy = accuracy_score(y_test, y_pred)
        report = classification_report(y_test, y_pred)
        matrix = confusion_matrix(y_test, y_pred)
        return accuracy, report, matrix

    def visualize_data(self):
        # Correlation matrix
        corr_matrix = self.data.corr()
        plt.figure(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', square=True)
        plt.title('Correlation Matrix')
        plt.show()

        # PCA
        pca = PCA(n_components=2)
        X_pca = pca.fit_transform(self.data.drop('target', axis=1))
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=X_pca[:, 0], y=X_pca[:, 1], hue=self.data['target'])
        plt.title('PCA')
        plt.show()

        # t-SNE
        tsne = TSNE(n_components=2)
        X_tsne = tsne.fit_transform(self.data.drop('target', axis=1))
        plt.figure(figsize=(8, 6))
        sns.scatterplot(x=X_tsne[:, 0], y=X_tsne[:, 1], hue=self.data['target'])
        plt.title('t-SNE')
        plt.show()

        # Class distribution
        plt.figure(figsize=(8, 6))
        sns.countplot(x=self.data['target'])
        plt.title('Class Distribution')
        plt.show()

    def handle_imbalance(self):
        X = self.data.drop('target', axis=1)
        y = self.data['target']
        counter = Counter(y)
        print('Original class distribution:', counter)

        # Oversampling
        smote = SMOTE(random_state=42)
        X_res, y_res = smote.fit_resample(X, y)
        counter = Counter(y_res)
        print('Oversampled class distribution:', counter)

        # Undersampling
        rus = RandomUnderSampler(random_state=42)
        X_res, y_res = rus.fit_resample(X, y)
        counter = Counter(y_res)
        print('Undersampled class distribution:', counter)

        return X_res, y_res

    def feature_importance(self, X, y):
       
