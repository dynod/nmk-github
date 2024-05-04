# Usage

To use this plugin in your **`nmk`** project, insert this reference in your **nmk.yml** main file:
```yaml
refs:
    - pip://nmk-github!plugin.yml
```

Then:
* a [workflow file](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions) is generated in order to handle your project build with **`nmk`** in Github CI
* Github related badges are added to your project's README.md file
