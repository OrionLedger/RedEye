import pandas as pd
from sklearn.preprocessing import StandardScaler

def standard_scale(df:pd.DataFrame):
    scaler = StandardScaler()

    numerical_cols = []
    for col in df.columns:
        if pd.api.types.is_integer_dtype(df[col]) or pd.api.types.is_float_dtype(df[col]):
            numerical_cols.append(col)

    df[numerical_cols] = scaler.fit_transform(df[numerical_cols])
    return df