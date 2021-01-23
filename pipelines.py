from dagster import pipeline
from solids import simple_solid, solid_with_annotations

@pipeline
def simple_hello_pipeline():
    simple_solid() 

@pipeline
def annotated_hello_pipeline():
    solid_with_annotations()