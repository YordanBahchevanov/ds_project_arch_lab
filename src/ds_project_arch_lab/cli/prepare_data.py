from __future__ import annotations
import argparse
from pathlib import Path
import pandas as pd

from ds_project_arch_lab.utils.preprocessing import standardize_column_names
from ds_project_arch_lab.features.build_features import FeatureConfig, prepare_feature_table


def parse_args() -> argparse.Namespace:
    p = argparse.ArgumentParser(description="Prepare features for asthma dataset.")
    p.add_argument("--input", type=Path, required=True, help="Input CSV (clean_asthma_disease_data.csv from Problem 3).")
    p.add_argument("--output-all", type=Path, required=True, help="Output: features + target CSV.")
    p.add_argument("--output-x", type=Path, default=None, help="Optional: X-only CSV.")
    p.add_argument("--output-y", type=Path, default=None, help="Optional: y-only CSV.")
    p.add_argument("--no-one-hot", action="store_true", help="Disable one-hot encoding of categoricals.")
    p.add_argument("--no-scale", action="store_true", help="Disable scaling of continuous features.")
    return p.parse_args()


def main() -> None:
    args = parse_args()

    df = pd.read_csv(args.input)
    df = standardize_column_names(df)

    cfg = FeatureConfig(
        one_hot_encode=not args.no_one_hot,
        scale_continuous=not args.no_scale,
    )
    feats = prepare_feature_table(df, cfg)

    args.output_all.parent.mkdir(parents=True, exist_ok=True)
    feats.to_csv(args.output_all, index=False)

    if args.output_x:
        X = feats.drop(columns=[cfg.target])
        Path(args.output_x).parent.mkdir(parents=True, exist_ok=True)
        X.to_csv(args.output_x, index=False)

    if args.output_y:
        y = feats[[cfg.target]]
        Path(args.output_y).parent.mkdir(parents=True, exist_ok=True)
        y.to_csv(args.output_y, index=False)

    print(f"Saved: {args.output_all}")
    if args.output_x: print(f"Saved: {args.output_x}")
    if args.output_y: print(f"Saved: {args.output_y}")


if __name__ == "__main__":
    main()
