from evidently.metrics import ClassificationQualityMetric, TextDescriptorsDriftMetric, ColumnDriftMetric
from evidently.pipeline.column_mapping import ColumnMapping
from evidently.report import Report
import json
import pandas as pd
import os

def check_drift():
# Get the directory of the current script
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the 'dataset' folder
    dataset_dir = os.path.join(script_dir, 'dataset')

    # Construct the full paths to the CSV files
    reference_path = os.path.join(dataset_dir, 'reference.csv')
    valid_disturbed_path = os.path.join(dataset_dir, 'valid_disturbed.csv')

    # Read the CSV files using the full paths
    reference = pd.read_csv(reference_path)
    valid_disturbed = pd.read_csv(valid_disturbed_path)

        # set up column mapping
    column_mapping = ColumnMapping()

    column_mapping.target = 'spam'
    column_mapping.prediction = 'predict_proba'
    column_mapping.text_features = ['email']

    # list features so text field is not treated as a regular feature
    column_mapping.numerical_features = []
    column_mapping.categorical_features = []

    data_drift_report = Report(
    metrics=[
        ColumnDriftMetric('spam'),
        ColumnDriftMetric('predict_proba'),
        TextDescriptorsDriftMetric(column_name='email'),
    ]
    )
    data_drift_report.run(reference_data=reference,
                        current_data=valid_disturbed,
                        column_mapping=column_mapping)
    
   
    report_json = json.loads(data_drift_report.json())
    dataset_drift_check = report_json['metrics'][2]['result']['dataset_drift']

    print(dataset_drift_check)
    return dataset_drift_check

if __name__ == "__main__":
    check_drift()
