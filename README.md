# NetworkGuardAI

NetworkGuardAI is a Python-based machine learning pipeline designed for network security analytics and threat detection. The project automates the ingestion, validation, transformation, and modeling of network data to help identify and mitigate potential security threats.

## Features

- **Automated Data Ingestion:** Extracts and stores network data from various sources, including CSV and MongoDB.
- **Data Validation:** Ensures incoming data matches defined schemas and validates the integrity of the datasets.
- **Data Transformation:** Cleans, imputes missing values, and prepares features for model training using pipelines.
- **Model Training:** Supports multiple classification algorithms (Logistic Regression, KNN, Decision Trees, Random Forest, AdaBoost, Gradient Boosting).
- **Model Evaluation:** Uses cross-validation and metrics to select the best-performing model.
- **Experiment Tracking:** Integrates with MLflow and DagsHub for model tracking and experiment management.

## Project Structure

```
main.py                       # Main entry point for running the training pipeline
push_data.py                  # Script for extracting and pushing network data to MongoDB
networksecurity/
    components/               # Data ingestion, validation, transformation, and model training components
    pipeline/                 # Training pipeline orchestration
    utils/                    # Utility functions (file I/O, evaluation, etc.)
```

## Getting Started

1. **Clone the repository**
    ```bash
    git clone https://github.com/Leerish/NetworkGuardAI.git
    cd NetworkGuardAI
    ```

2. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```

3. **Configure your environment**
    - Set up your MongoDB connection and adjust paths as needed in the config files.

4. **Run the training pipeline**
    ```bash
    python main.py
    ```

## Example Workflow

1. Data is ingested from source files or MongoDB and split into training/testing sets.
2. Data validation checks for schema and data drift issues.
3. Data transformation handles missing values and feature engineering.
4. Multiple models are trained and evaluated. The best model is saved and tracked.

## Technologies Used

- Python
- scikit-learn
- pandas, numpy
- MLflow, DagsHub
- MongoDB

## License

This project is currently unlicensed.

## Author

- [Leerish](https://github.com/Leerish)

---
> **Note**: This project is under active development. Contributions and suggestions are welcome!
