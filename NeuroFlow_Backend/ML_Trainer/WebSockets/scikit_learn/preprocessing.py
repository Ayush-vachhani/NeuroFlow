import pandas as pd


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
