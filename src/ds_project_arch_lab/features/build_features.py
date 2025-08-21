from __future__ import annotations
from dataclasses import dataclass, field
from typing import List, Optional, Sequence
import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler


@dataclass
class FeatureConfig:
    target: str = "diagnosis"
    categorical: Sequence[str] = ("gender", "ethnicity", "education_level")
    continuous: Sequence[str] = (
        "age", "bmi", "physical_activity", "diet_quality", "sleep_quality",
        "pollution_exposure", "pollen_exposure", "dust_exposure",
        "lung_function_fev1", "lung_function_fvc",
    )
    symptom_cols: Sequence[str] = (
        "wheezing", "shortness_of_breath", "chest_tightness",
        "coughing", "nighttime_symptoms", "exercise_induced",
    )
    exposure_cols: Sequence[str] = ("pollution_exposure", "pollen_exposure", "dust_exposure")

    add_fev1_fvc_ratio: bool = True
    add_symptom_score: bool = True
    add_exposure_index: bool = True

    one_hot_encode: bool = True
    drop_first: bool = True
    scale_continuous: bool = True

    drop_cols: Sequence[str] = ("patientid", "doctor_in_charge")


def engineer_features(df: pd.DataFrame, cfg: FeatureConfig) -> pd.DataFrame:
    out = df.copy()

    if cfg.add_fev1_fvc_ratio and {"lung_function_fev1", "lung_function_fvc"}.issubset(out.columns):
        out["fev1_fvc_ratio"] = (out["lung_function_fev1"] / out["lung_function_fvc"]).replace([np.inf, -np.inf], np.nan)

    use_symptoms = [c for c in cfg.symptom_cols if c in out.columns]
    if cfg.add_symptom_score and use_symptoms:
        out["symptom_score"] = out[use_symptoms].sum(axis=1)

    use_exposures = [c for c in cfg.exposure_cols if c in out.columns]
    if cfg.add_exposure_index and use_exposures:
        out["exposure_index"] = out[use_exposures].mean(axis=1)

    return out


def encode_categoricals(df: pd.DataFrame, cfg: FeatureConfig) -> pd.DataFrame:
    if not cfg.one_hot_encode:
        return df
    use_cats = [c for c in cfg.categorical if c in df.columns]
    return pd.get_dummies(df, columns=use_cats, drop_first=cfg.drop_first)


def scale_continuous(df: pd.DataFrame, cfg: FeatureConfig) -> pd.DataFrame:
    if not cfg.scale_continuous:
        return df
    out = df.copy()
    to_scale = [c for c in list(cfg.continuous) + ["fev1_fvc_ratio", "symptom_score", "exposure_index"]
                if c in out.columns]
    if to_scale:
        scaler = StandardScaler()
        out[to_scale] = scaler.fit_transform(out[to_scale])
    return out


def prepare_feature_table(df: pd.DataFrame, cfg: FeatureConfig) -> pd.DataFrame:
    """
    Full feature pipeline (no file I/O): drop columns -> engineer -> encode -> scale -> float table.
    Returns a numeric, float-only dataframe with target column preserved.
    """
    from ds_project_arch_lab.utils.preprocessing import drop_columns, ensure_float_table

    out = drop_columns(df, cfg.drop_cols)
    out = engineer_features(out, cfg)
    out = encode_categoricals(out, cfg)
    out = scale_continuous(out, cfg)
    out = ensure_float_table(out, cfg.target)
    return out
