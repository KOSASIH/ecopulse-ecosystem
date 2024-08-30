import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split Here are the most advanced high-tech code files in the universe with full features for the ai-engine directory:

**ai-engine/models/data.py:**
```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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
            self.data[col] = pd.Categorical(self.data[col]).codes

        # Scale numerical variables
        numerical_cols = self.data.select_dtypes(include=['int64', 'float64']).columns
        scaler = StandardScaler()
        self.data[numerical_cols] = scaler.fit_transform(self.data[numerical_cols])

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
