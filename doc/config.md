# Configuration Reference

The **`nmk-github`** plugin handles the configuration items listed in this page.

All of them are initiliazed with convenient default values, so that you don't need to setup them for a default working behavior. You can anyway override them in your projet if you need to fine tune the plugin behavior. [Some items](extend.md) are specifically designed to be extended by **`nmk`** projects and plugins.

## Project information

(githubUser)=
### **`githubUser`** -- user name for this Github project

| Type | Default value |
|-     |-
| str  | Resolved by {py:class}`nmk_github.info.GithubUserResolver`

User name for this Github project, deduced from remote git URL.

(githubRepo)=
### **`githubRepo`** -- repository name for this Github project

| Type | Default value |
|-     |-
| str  | Resolved by {py:class}`nmk_github.info.GithubRepoResolver`

Repository name for this Github project, deduced from remote git URL.

## Actions

(githubAction)=
### **`githubAction`** -- target Github workflow file

| Type | Default value |
|-     |-
| str  | ${PROJECTDIR}/.github/workflows/build.yml

Target workflow file containing CI job definition in reaction to push operations to the remote Github repository. This file is the output of the **{ref}`gh.actions<actionsTask>`** task.

(githubActionTemplate)=
### **`githubActionTemplate`** -- workflow file template

| Type | Default value |
|-     |-
| str  | ${BASEDIR}/templates/build.yml

Jinja template used to generate the **{ref}`${githubAction}<githubAction>`** workflow file.

(githubPythonVersions)=
### **`githubPythonVersions`** -- python versions for Github workflows manual configuration

| Type | Default value |
|-     |-
| List[str]  | []

List of python versions to be used in Github workflow (manual configuration).

(githubDetectedPythonVersions)=
### **`githubDetectedPythonVersions`** -- python versions for Github workflows detected configuration

| Type | Default value |
|-     |-
| List[str]  | Resolved by {py:class}`nmk_github.action.PythonVersionsResolver`

List of python versions to be tested in Github actions. Returns:

* **{ref}`${githubPythonVersions}<githubPythonVersions>`** if set
* otherwise if **`nmk-python`** plugin is used, the supported python versions range will be returned instead
* otherwise returns []

(githubOSImages)=
### **`githubOSImages`** -- OS images for Github actions

| Type | Default value |
|-     |-
| List[str]  | ["ubuntu-latest", "windows-latest"]

List of operating systems (build images) for Github actions

(githubCommand)=
### **`githubCommand`** -- Build command for Github actions

| Type | Default value |
|-     |-
| str  | "./buildenv.sh run nmk tests"

Command string to perform **`nmk`** build (+ tests) while running Github actions

(githubBuildSteps)=
### **`githubBuildSteps`** -- Github build workflow steps contribution

| Type | Default value |
|-     |-
| List[Dict]  | []

A list of extra Github build workflow steps, to be executed after build command.

Expected to be a list of objects, that will be serialized in generated **{ref}`${githubAction}<githubAction>`** file.

Special keys for each object:
* **`__if__`**: when set, generate this step if the provided condition is met
* **`__unless__`**: when set, generate this step unless the provided condition is met


(githubPublishSteps)=
### **`githubPublishSteps`** -- Github publish workflow steps contribution

| Type | Default value |
|-     |-
| List[Dict]  | []

A list of extra Github publish workflow steps, to be executed after build command.

Expected to be a list of objects, that will be serialized in generated **{ref}`${githubAction}<githubAction>`** file.

Special keys for each object:
* **`__if__`**: when set, generate this step if the provided condition is met
* **`__unless__`**: when set, generate this step unless the provided condition is met

## Badges

Following items help to configure generated badges related to Github details.

(githubLicense)=
### **`githubLicense`** -- License used by Github project

| Type | Default value |
|-     |-
| str  | "MPL"

License name configuration (default to Mozilla Public License).

(githubIssuesRepo)=
### **`githubIssuesRepo`** -- Github repository hosting issues

| Type | Default value |
|-     |-
| str  | **{ref}`${githubRepo}<githubRepo>`**

Github repository hosting issues for this project (default to current repository).

(githubIssuesLabel)=
### **`githubIssuesLabel`** -- Github issues query optional label

| Type | Default value |
|-     |-
| str  | ""

Optional label used when querying issues for this repository.

(githubIssuesLabelSuffix)=
### **`githubIssuesLabelSuffix`** -- Github issues query optional label

| Type | Default value |
|-     |-
| str  | Resolved by {py:class}`nmk_github.info.GithubIssuesLabelResolver`

Query suffix for extra label provided by **{ref}`${githubIssuesLabel}<githubIssuesLabel>`**.
