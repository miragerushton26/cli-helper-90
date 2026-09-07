import functools
import logging

class DataProcessor:
    def __init__(self, settings=None):
        self.settings = settings or {}
        self.pipeline = []

    def register_step(self, func):
        self.pipeline.append(func)
        return func

    def execute(self, data):
        return functools.reduce(lambda acc, step: step(acc), self.pipeline, data)

def sanitize_input(data):
    if isinstance(data, str):
        return data.strip().lower()
    return data

def transform_to_list(data):
    return [data] if not isinstance(data, list) else data

def run_pipeline(input_data):
    proc = DataProcessor()
    proc.register_step(sanitize_input)
    proc.register_step(transform_to_list)
    try:
        return proc.execute(input_data)
    except Exception as e:
        logging.error(f"pipeline failure: {e}")
        return []

if __name__ == "__main__":
    result = run_pipeline("  SAMPLE_DATA  ")
    print(result)