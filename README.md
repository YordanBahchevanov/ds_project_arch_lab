# ds_project_arch_lab

Lab project with Poetry, src layout, and data pipeline.

## Project structure

├─ config/ # configuration files (YAML)
├─ data/ # datasets (not tracked in Git)
│ ├─ raw/ # original data
│ ├─ interim/ # cleaned/processed during pipeline
│ └─ processed/ # features ready for modeling
├─ notebooks/ # Jupyter notebooks (EDA, experiments)
├─ reports/ # figures and outputs
│ └─ figures/
├─ src/ # source code (pipeline, utils, models)
├─ tests/ # unit tests
├─ pyproject.toml # Poetry project definition
├─ poetry.lock # locked dependencies
└─ README.md

## Data

This project uses the **asthma dataset** from [Kaggle](https://www.kaggle.com/datasets/rabieelkharoua/asthma-disease-dataset).

The dataset is **not stored in GitHub** (to keep the repo small and because data is ignored via `.gitignore`).  
To run the notebooks or pipeline, download the dataset and place it in: data/raw/asthma_disease_data.csv


> Note: The course platform already preloads the dataset into `data/`, so you may not need to download it manually.

## Environment setup

1. **Install Poetry**  
   Follow the [Poetry installation guide](https://python-poetry.org/docs/#installation).

2. **Clone this repo**
   ```powershell
   git clone https://github.com/YordanBahchevanov/ds_project_arch_lab.git
   cd ds_project_arch_lab

3. **Install dependencies**
    poetry install

4. **Register Jupyter kernel**
    poetry run python -m ipykernel install --user --name ds-project-arch-lab --display-name "Python (ds-project-arch-lab)"

## Usage

1. Do your exploration and research in notebooks under notebooks/.

2. Reusable pipeline code should live under src/ds_project_arch_lab/.

3. Unit tests should go in tests/.

4. MLflow will track experiments locally in the mlruns/ directory (ignored by Git).