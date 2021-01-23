from dagster import repository
from pipelines import simple_hello_pipeline, annotated_hello_pipeline


@repository
def my_repo():
    return {
        "pipelines": {
            "simple_hello_pipeline": simple_hello_pipeline,
            "annotated_hello_pipeline": annotated_hello_pipeline
        }
    }
