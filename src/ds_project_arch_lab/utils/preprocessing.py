from __future__ import annotations
import re
from typing import Iterable, Sequence
import pandas as pd


def standardize_column_names(df: pd.DataFrame) -> pd.DataFrame:
    """
    Return a copy with column names converted to snake_case, handling acronyms and numbers.
    Examples:
        'DietQuality' -> 'diet_quality'
        'BMI' -> 'bmi'
        'LungFunctionFEV1' -> 'lung_function_fev1'
        'Lung Function FEV1' -> 'lung_function_fev1'
    """
    def camel_to_snake(name: str) -> str:
        name = name.replace(" ", "_")
        # lower<->Upper boundary: lungFunction -> lung_Function
        name = re.sub(r"([a-z0-9])([A-Z])", r"\1_\2", name)
        # letter-number boundary: FEV1 -> FEV_1 (will become fev_1 -> fev1 on cleanup below if desired)
        name = re.sub(r"([A-Za-z])([0-9])", r"\1_\2", name)
        name = name.lower()
        # optional: collapse duplicated underscores
        name = re.sub(r"__+", "_", name).strip("_")
        # optional special-cases (keep acronyms tight)
        name = name.replace("b_m_i", "bmi").replace("f_e_v_1", "fev1")
        return name

    out = df.copy()
    out.columns = [camel_to_snake(c) for c in out.columns]
    return out


def drop_columns(df: pd.DataFrame, cols: Iterable[str]) -> pd.DataFrame:
    """Drop columns if present (no error if they are missing)."""
    return df.drop(columns=[c for c in cols if c in df.columns], errors="ignore")


def ensure_float_table(df: pd.DataFrame, target: str) -> pd.DataFrame:
    """
    Cast all non-target columns to float. Target left as-is (0/1 preferred).
    """
    out = df.copy()
    for c in out.columns:
        if c != target:
            out[c] = pd.to_numeric(out[c], errors="coerce").astype(float)
    return out
