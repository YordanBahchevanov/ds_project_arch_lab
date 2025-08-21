import pandas as pd
import re


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy of DataFrame with column names standardized to lowercase snake_case.
    
    Examples:
        'DietQuality' -> 'diet_quality'
        'SleepQuality' -> 'sleep_quality'
        'BMI' -> 'bmi'
        'LungFunctionFEV1' -> 'lung_function_fev1'
    """
    def camel_to_snake(name: str) -> str:
        # Replace spaces with underscores
        name = name.replace(" ", "_")
        # Handle acronym/number groups properly:
        # 1. Put underscore between a lower & upper case letter (e.g., "lungFunction" -> "lung_Function")
        name = re.sub(r'([a-z0-9])([A-Z])', r'\1_\2', name)
        # 2. Put underscore between a letter and a number (e.g., "FEV1" -> "FEV_1")
        name = re.sub(r'([A-Za-z])([0-9])', r'\1_\2', name)
        # 3. Lowercase everything
        return name.lower()
    
    df_copy = df.copy()
    df_copy.columns = [camel_to_snake(col) for col in df_copy.columns]
    return df_copy
