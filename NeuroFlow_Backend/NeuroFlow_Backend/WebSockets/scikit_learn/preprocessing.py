import json
import pandas as pd
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split
import numpy as np


def preprocess_data(df, is_train=True):
    df_processed = df.drop(['Name', 'Ticket', 'Cabin', 'Embarked'], axis=1)

    # Convert 'Sex' to a binary feature
    df_processed['Sex'] = df_processed['Sex'].map({'male': 0, 'female': 1})

    # Handle missing values
    df_processed.fillna(0, inplace=True)

    # Separate features and target if it's a training set
    if is_train:
        X = df_processed.drop('Survived', axis=1)
        Y = df_processed['Survived']
        return X, Y
    else:
        return df_processed, None


async def train_and_evaluate_classifier(self, classifier, params):
    df = pd.read_csv('Data/Titanic/train.csv')
    np.random.seed(42)
    # Preprocess the data
    X, Y = preprocess_data(df)

    # Split the data into training and validation sets
    X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2)
    # Initialize and train the model
    model = classifier(**params)
    model.fit(X_train, Y_train)

    # Evaluate the model
    accuracy = accuracy_score(Y_val, model.predict(X_val))
    await self.send(text_data=json.dumps({
        'message': f'Trained and tested model with accuracy: {accuracy}'
    }))
    print(f'Trained and tested model with accuracy: {accuracy}')
