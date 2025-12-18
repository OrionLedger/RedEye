import pandas as pd
from sklearn.preprocessing import LabelEncoder, OneHotEncoder

def cat_label_features_encoder(df: pd.DataFrame):
    categorical_cols = [col for col in df.columns if pd.api.types.is_object_dtype(df[col]) and df[col].nunique() > 5]
    encoders = {}
    for col in categorical_cols:
        encoder = LabelEncoder()
        df[col] = encoder.fit_transform(df[col])
        encoders[col] = encoder
    return df

def one_hot_features_encoder(df: pd.DataFrame):
    categorical_cols = [col for col in df.columns if pd.api.types.is_object_dtype(df[col]) and df[col].nunique() <= 5]
    if not categorical_cols:
        return df
    encoder = OneHotEncoder(sparse_output=False, handle_unknown='ignore')
    encoded_array = encoder.fit_transform(df[categorical_cols])
    encoded_df = pd.DataFrame(
        encoded_array,
        columns=encoder.get_feature_names_out(),
        index=df.index
    )
    df = pd.concat([df.drop(columns=categorical_cols), encoded_df], axis=1)
    return df


