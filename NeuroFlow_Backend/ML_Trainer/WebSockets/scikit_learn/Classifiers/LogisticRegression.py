import numpy as np
import pandas as pd
import json
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from ML_Trainer.WebSockets.scikit_learn.preprocessing import preprocess_data


async def train_logistic_regression(self, params):
    np.random.seed(42)
    try:
        # Load the dataset
        df = pd.read_csv('Data/Titanic/train.csv')

        # Preprocess the data
        X, Y = preprocess_data(df)

        # Split the data into training and validation sets
        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2)

        # Extract parameters or use defaults
        C = params.get('C')
        penalty = params.get('penalty')
        max_iter = params.get('max_iter')
        # Train the model
        model = LogisticRegression(max_iter=max_iter, C=C)
        model.fit(X_train, Y_train)
        # Evaluate the model
        print(f'Model fitting complete. Evaluating...')
        predictions = model.predict(X_val)
        accuracy = accuracy_score(Y_val, predictions)

        # Send the result back
        await self.send(text_data=json.dumps({
            'message': f'Trained and tested model with accuracy: {accuracy}'
        }))
        print(f'Trained and tested model with accuracy: {accuracy}')
    except Exception as e:
        await self.send(text_data=json.dumps({
            'error': str(e)
        }))