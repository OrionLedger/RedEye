from sklearn.preprocessing import PowerTransformer
import pandas as pd
import numpy as np

def log_transform(df:pd.DataFrame):
    numeric = df.select_dtypes(include=['number'])
    log_transformer = PowerTransformer(method='yeo-johnson')
    numeric = pd.DataFrame(log_transformer.fit_transform(numeric), columns=log_transformer.get_feature_names_out())
    df[numeric.columns] = numeric

    return df