# Dagster Learnings

## What is dagster?
dagster is a Python workflow or task orchestration library.  Why is this useful?  Let's say you have a handful of tasks or more (a collection of tasks also referred to as a "pipeline") that need to be all executed in an organized way, with dependencies between tasks fulfilled.  If using just pure Python code that you rolled up on your own, whether using functions with IF-ELSE logic, or some other cobbled together logic, this can get very unmanageable or fragile, not to mention, trying to somehow handle failures of one or more of your tasks.  Do you just re-run all tasks?  But, what if a task or two takes several minutes?  Wouldn't it be great to execute just the tasks that failed?  Again, trying to implement this by yourself with pure Python code would be a nightmare.  That is why frameworks or libraries like dagster exist.  A workflow or task orchestration library is very useful in an environment where there is a strong need for automation.  Other well-known Python workflow or task orchestration libraries include Apache Airflow and Spotify Luigi.  dagster and prefect are the newest generation of task orchestration libraries, created 2 and 3 years ago, respectively, at the time of this writing.

## How to get started with dagster
To get started with dagster, you just simply `pip install dagster dagit`.  Then set the environment variable `DAGSTER_HOME` and dump your [dagster.yaml](config/dagster.yaml) file there.  That's it.  No esoteric or complex configuration needed.  The only time there is additional configuration is if you are in need of using its advanced options or using a different database backend like PostgreSQL, instead of the default sqlite backend.  Then after that, at minimum you code Python functions decorated with the `@solid` decorator and define a pipeline.  Optionally, you could also define repository/ies or workspace(es) to better organize your data pipelines. 

## Is dagster easy to use?
If you have at least intermediate Python knowledge, then you can easily handle dagster.  My caveat is that some parts of the tutorial in their documentation is a bit complex and there is some boilerplate code, but most of the boilerplate is isolated to just their `@solid` decorator.  Another thing to get used to is that the dagster API can be unexpectedly strict or opinionated in some areas, especially with data types.  If you have been using Python's type annotations, then you will be able to quickly adjust.  If you don't know what type annotations are, then I do NOT recommend using dagster until you have some familiarity.  But it takes very little time to learn (a few hours or maybe a day).  With non-standard Python data types or data structures (ex. pandas dataframes), you are forced to use dagster's own data types.  You should also have familiarity working with YAML files.  Working with YAML files is also very easy to learn.  It is just a text file where you arrange one or more key, value combinations in an indent-structured format (usually 2 spaces of indentation).

**pre-requisites:**

- Intermediate Python knowledge
- Type annotation experience
- Working with YAML file format


## High-level overview of dagster
To understand dagster, you have to be familiar with its abstraction hierarchies:<br>
[workspace](https://docs.dagster.io/overview/repositories-workspaces/workspaces) <- [repository](https://docs.dagster.io/overview/repositories-workspaces/repositories) <- [pipeline](https://docs.dagster.io/overview/solids-pipelines/pipelines) <- [solid](https://docs.dagster.io/overview/solids-pipelines/solids)

#### Workspace
A workspace is dagster's highest hierarchy abstraction.  It is a spec (defined in a YAML file) to tell dagster about the Python source code, Python environment, and repositories you are working with.  What is useful about this is we can run pipelines tailored for a specific Python environment, instead of a single, monolithic Python environment.

#### Repository
A repository is a collection of pipelines

#### Pipeline
A pipeline is a collection of tasks (in dagster's world or terminology, a task is a "solid")

#### Solid
A solid is a task or Python function decorated with `@solid` decorator

#### References
workspace: https://docs.dagster.io/overview/repositories-workspaces/workspaces<br>
repository: https://docs.dagster.io/overview/repositories-workspaces/repositories

# Thoughts on dagster API after a few weeks of use
Although I find dagster relatively simple to use, what can be surprising is how tightly coupled its API is with its web UI called `dagit`, even though you are not required to use `dagit`.

What this means, its boilerplate and configuration code is directly proportional to how much you want to get out of its `dagit` web UI.
If you want less boilerplate, then use less code tied to dagit.

So why would one want to have an optional need for this boilerplate code?  What is useful and perhaps unique with dagster, it allows us to add informative annotations or metadata to our pipelines which are accessible in the `dagit` web UI.  Basically, we can think of these annotations as "sticky notes" that we place on our data as it is traveling through the pipeline.  What this essentially allows us to do is, we are able to "poke and prod" our data, inspect that the data we received, created, transformed, or sent is what we expect it to be, which in the end, allows us to easily prototype, debug, and test our pipeline.  This ability however, has its consequences, one of which is more boilerplate code.  However, as mentioned previously, dagster does not force you to use dagit or its pipeline annotations or metadata features.  dagster comes with an option to use a pure Python interface, a CLI, or you can use dagit.  You can view these 2 [solids](solids.py) in this repo to compare a simple solid against another solid with annotations or metadata.

More specifically, a few examples of things that can add boilerplate to your code:
- [InputDefinitions](https://docs.dagster.io/tutorial/types#mypy-compliance)
- [OutputDefinitions](https://docs.dagster.io/tutorial/types#mypy-compliance)
- yielding [AssetMaterializations](https://docs.dagster.io/tutorial/advanced_materializations)

The items above are OPTIONAL and tied to adding useful annotations/metadata to your pipeline in `dagit`.  These extra niceties are useful for those who want to have intimate knowledge about their data processes, which will tend to be business side users who have a stake in the quality of their data.  dagster is an especially useful tool for business side data engineers.

One thing of note, solid parameters usually fall into one of 2 categories in dagster:
- parameters that are actual [inputs](https://docs.dagster.io/tutorial/basics_solids#parametrizing-solids-with-inputs) to the solid
- parameters that are not actual inputs to the solid and are then defined in the "[config_schema](https://docs.dagster.io/tutorial/basics_solids#parametrizing-solids-with-config)"

Another thing of note, generally, dagster expects solids to have input(s) and then give out output(s).  But there are instances where a solid don't necessarily need to have input or provide output.  In this case, use their built-in `Nothing` type: https://docs.dagster.io/examples/nothing

## What do I like about dagster?

- It is a general purpose scheduler - therfore, can be used in a variety of use cases (automation, ETL, machine learning, etc)
- You can develop locally and then deploy on cloud platform
- Its facility to add annotations or metadata to the pipeline is extremely useful to get more "hands-on" with the data, which aids in debugging or testing the pipeline
- It comes with an amazing web UI (dagit) with real-time tracking of your pipelines
- Easily manage and organize multiple pipelines.  It is easy to execute pipelines specifically tailored for various groups or organizations due to the notion of workspace and repository aspects of dagster.
- It fully works on Windows and no special admin privileges required
- It comes with a native scheduler - no need to rely on Windows Task Scheduler or 'NIX OS cron.  You can even use cron syntax to define finely-grained scheduling intervals.
- Event-based triggering via `sensors` and `hooks` (send a Slack or MS Teams notification when a pipeline fails or when a file is saved onto a network share drive)

## What do I not like about dagster?

- There is a bit of boilerplate code, but which you can control for the most part
- A bit opinionated in a few areas: you are forced to use dagster's data type for non-standard Python data types or data structures (ex. you can't use pd.DataFrame, but have to use dagster's DataFrame type)
- Unclear usage of `composite-solid`, but which will be removed in version 0.11.x
- Documentation can be lacking for certain patterns or use cases.  For example, it is not immediately apparent how to re-execute pipeline at point of failure using the CLI or Python API.  Also, to be able to pass data between solids, you have to set IO manager to a persistent IO manager such as `fs_io_manager`, by definign mode definition within your `@solid` decorator.  This is a bit more boilerplate also.

## Can it be used for mission-critical pipelines?
Maybe? It is a relatively young library (only 2 years old) and its API has only recently stabilized.  Version 0.10.0 is probably the best version to start using dagster.

## Executing the example pipelines
With dagster, you have a few different options to execute the example pipelines in this repo:

**via dagit web UI**<br>
`dagit -f repository.py`

**via CLI**<br>
To execute the simple_hello_pipeline:<br>
`dagster pipeline execute -f repository.py --pipeline simple_hello_pipeline -c simple_solid_config.yaml`<br>
or<br>
To execute the annotated_hello_pipeline:<br>
`dagster pipeline execute -f repository.py --pipeline annotated_hello_pipeline -c annotated_solid_config.yaml`<br>

**via Python "main" method**<br>
`python solids.py`