import numpy as np
import pandas as pd
import json
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

from ML_Trainer.WebSockets.scikit_learn.preprocessing import preprocess_data


async def train_decision_trees(self, params):
    np.random.seed(42)
    try:
        # Load the dataset
        df = pd.read_csv('Data/Titanic/train.csv')

        # Preprocess the data
        X, Y = preprocess_data(df)

        # Split the data into training and validation sets
        X_train, X_val, Y_train, Y_val = train_test_split(X, Y, test_size=0.2)

        # Extract parameters or use defaults
        max_depth = params.get('max_depth')
        min_samples_split = params.get('min_samples_split')

        # Train the model
        model = DecisionTreeClassifier(min_samples_split=min_samples_split, max_depth=max_depth)
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
