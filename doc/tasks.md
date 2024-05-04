# Tasks

The **`nmk-github`** plugin defines the tasks described below.

## Setup tasks

All tasks in this chapter are dependencies of the base [**`setup`**](https://nmk-base.readthedocs.io/en/stable/tasks.html#setup-task) task.

(actionsTask)=
### **`gh.actions`** -- workflow file generation

This tasks generate the **{ref}`${githubAction}<githubAction>`** workflow file.

| Property | Value/description |
|-         |-
| builder  | {py:class}`nmk_github.action.ActionFileBuilder`
| input    | **{ref}`${githubActionTemplate}<githubActionTemplate>`** template file
| output   | **{ref}`${githubAction}<githubAction>`** workflow file

The builder is invoked with the following parameters mapping:

| Name | Value |
|- |-
| python_versions | **{ref}`${githubDetectedPythonVersions}<githubDetectedPythonVersions>`**
| command | **{ref}`${githubCommand}<githubCommand>`**
| images | **{ref}`${githubOSImages}<githubOSImages>`**
| build_steps | **{ref}`${githubBuildSteps}<githubBuildSteps>`**
| publish_steps | **{ref}`${githubPublishSteps}<githubPublishSteps>`**

This task is enabled only if python supported version(s) are configured (see **{ref}`${githubDetectedPythonVersions}<githubDetectedPythonVersions>`**)

The generated Github workflow implements the following steps:

* On branch push:
    * parallelizes multiple jobs for all combinations of **{ref}`${githubDetectedPythonVersions}<githubDetectedPythonVersions>`** and **{ref}`${githubOSImages}<githubOSImages>`** values
    * launches **{ref}`${githubCommand}<githubCommand>`** build command
    * launches extra steps defined by **{ref}`${githubBuildSteps}<githubBuildSteps>`**

* On tag push:
    * runs a single job on a default configuration (linux + python 3.8)
    * launches **`./buildenv.sh run nmk build git.dirty`** build command
    * launches extra steps defined by **{ref}`${githubPublishSteps}<githubPublishSteps>`**
