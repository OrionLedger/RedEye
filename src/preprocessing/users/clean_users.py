import pandas as pd
from sklearn.impute import SimpleImputer

def clean_users(df: pd.DataFrame):
    df.dropna(axis=0)
    numeric_columns = []
    print ("Columns Are: ", df.columns)
    for col in list(df.columns):
        if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            numeric_columns.append(col)

    numeric_df = df[numeric_columns]
    imputer = SimpleImputer(strategy='mean')
    df[numeric_columns] = imputer.fit_transform(numeric_df)

    return df