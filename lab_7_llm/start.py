"""
Neural machine translation starter.
"""
# pylint: disable= too-many-locals
from core_utils.llm.time_decorator import report_time
from config.constants import PROJECT_ROOT
from lab_7_llm.main import RawDataImporter, RawDataPreprocessor, TaskDataset, LLMPipeline
from torch.utils.data import DataLoader, Dataset
import pandas as pd
import json

@report_time
def main() -> None:
    """
    Run the translation pipeline.
    """
    with open(PROJECT_ROOT / 'lab_7_llm' / 'settings.json', 'r', encoding='utf-8') as settings:
        settings = json.load(settings)
    govreport = RawDataImporter('ccdv/govreport-summarization')
    govreport.obtain()
    preprocessor = RawDataPreprocessor(govreport.raw_data)
    preprocessor.transform()
    result = preprocessor.analyze()
    dataset = TaskDataset(preprocessor._data.head(100))
    pipeline = LLMPipeline(settings['parameters']['model'],
                           dataset,
                           max_length=120,
                           batch_size=5,
                           device='cpu')

    pipeline.analyze_model()
    pipeline.infer_sample(dataset[0])

    """dataset_loader = DataLoader(dataset, batch_size=4)
    pipeline = LLMPipeline(settings['parameters']['model'], dataset, 100, 100, 'cpu')
    pipeline.analyze_model()"""
    assert result is not None, "Demo does not work correctly"


if __name__ == "__main__":
    main()
