from dagster import (
    execute_pipeline,
    pipeline,
    solid,
    AssetMaterialization,
    Bool,
    EventMetadataEntry,
    Field,
    InputDefinition,
    OutputDefinition,
    Output,
    Nothing,
    String
)

# A dagster solid with minimal boilderplate code
# Since param is not an actual input to this solid, dagster recommends non-input parameters
# be defined in config_schema, see https://docs.dagster.io/tutorial/basics_solids
# in section titled "Parameterizing Solids with Config"
@solid(config_schema={'param': bool})
def simple_solid(context, name: str) -> None:
    var1 = context.solid_config['param']

    context.log.info(f'**** param: {var1}')

    if var1:
        context.log.info(f'Hello {name}!')
    else:
        context.log.info('Hello NoName!')


# A solid example with more boilerplate code to add annotations or metadata to dagit
@solid(
    description="A solid to exemplify boilderplate code when adding annotations",
    config_schema={
        'param': Field(Bool, is_required=False, default_value=True)
    },
    input_defs=[
        InputDefinition(
            name="name",
            description="A person's name",
            dagster_type=String,
            default_value="John Doe"
        )
    ],
    output_defs=[
        OutputDefinition(
            name="MyName",
            dagster_type=String
        )
    ]
)
def solid_with_annotations(context, name: str) -> String:
    var1 = context.solid_config['param']

    context.log.info(f'**** param: {var1}')

    if var1:
        context.log.info(f'Hello {name[::-1]}!')
        yield AssetMaterialization(
            asset_key="name_asset",
            description="Name spelled backwards if param is True",
            metadata_entries=[
                EventMetadataEntry.text(
                    text=f'Hello {name[::-1]}!',
                    label='When True'
                )
            ]
        )
    else:
        context.log.info('Hello NoName!')
        yield AssetMaterialization(
            asset_key="name_asset",
            description="Returns NoName if param is False",
            metadata_entries=[
                EventMetadataEntry.text(
                    text=f'Hello NoName!',
                    label='When False'
                )
            ]
        )
    yield Output(value=name, output_name="MyName")


# In dagit, this is what you would enter in the Playground editor:
# solids:
#   solid_with_annotations:
#     inputs:
#       name: "NameIsBackwords"
#     config:
#       param: True


# Un-comment the lines below if you want to execute this pipeline
# via CLI

simple_config = {
    "solids": {
        "simple_solid": {
            "inputs": {"name": {"value": "Daniel"}},
            "config": {"param": True}
        }
    }
}

annotated_config = {
    "solids": {
        "solid_with_annotations": {
            "inputs": {"name": {"value": "Daniel"}},
            "config": {"param": True}
        }
    }
}

@pipeline
def simple_hello_pipeline():
    simple_solid()

@pipeline
def annotated_hello_pipeline():
    solid_with_annotations()


if __name__ == "__main__":
    simple_hello_result = execute_pipeline(simple_hello_pipeline,
        run_config=simple_config
    )

    annotated_hello_result = execute_pipeline(annotated_hello_pipeline,
        run_config=annotated_config
    )