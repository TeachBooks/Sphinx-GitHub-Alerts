# Sphinx GitHub Alerts

## Introduction

This Sphinx extension converts GitHub alerts to Sphinx admonitions.

## What does it do?

This extension allows you to use [GitHub alerts](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax#alerts) within your Sphinx project. This is particulary useful if you're editing your sphinx / jupyterbook / teachbook in GitHub, making use of GitHub alerts and the markdown previewer of GitHub. Your Sphinx project will look similar to the preview in GitHub for these GitHub alerts.

Only top-level alerts are allowed and are convert to a top-level admonition in the language (`MD` or `rST`) of the source file. The source file does not change.

Nesting is not supported.

If an alert is not recognised, a warning is returned.

## Installation

To use this extension, follow these steps:

**Step 1: Install the Package**

Install the module `sphinx-github-alerts` package using `pip`:
```
pip install sphinx-github-alerts
```
    
**Step 2: Add to `requirements.txt`**

Make sure that the package is included in your project's `requirements.txt` to track the dependency:
```
sphinx-github-alerts
```

**Step 3: Enable in `_config.yml` or `conf.py`**

In your `_config.yml` file, add the extension to the list of Sphinx extra extensions (**important**: underscore, not dash this time):

```yaml
sphinx: 
    extra_extensions:
        .
        .
        .
        - sphinx_github_alerts
        .
        .
        .
```

or in your `conf.py` file, add the extension to the `extensions` list and specify the location of your bib file:

```python
extensions = [...,"sphinx_github_alerts",...]
```

## Configuration

The extension provides several configuration values, which can be added to your configuration file:

- `sphinx_github_alerts_backquotes`: `3` (_default_) or `integer`: (only relevant for MarkDown based files) The number of backticks used to start and end the admonitions. Should be at minimum 3.
- `sphinx_github_alerts_leading_spaces`: `3` (_default_) or `integer`: (only relevant for reStructeredText based files) The number of spaces for indentation within the admonitions. Should be at minimum 1.
- `sphinx_github_alerts_redirects`: `{}`  (_default_) or `dict`: Every _key_-**value** pair in this dictionary redirects the GitHub alert indicated by _key_ to the Sphinx admonition indicated by **value**.

## Examples

For each of the five GitHub alerts, you can see the result below. Note that the result depends on where you are visiting this page.

The codes contain a leading space to enforce showing the code and not converting the code. In any application these leading spaces should not be present.

### Note

```
 > [!NOTE]
 > Useful information that users should know, even when skimming content.
```

> [!NOTE]
> Useful information that users should know, even when skimming content.

### Tip

```
 > [!TIP]
 > Helpful advice for doing things better or more easily.
```

> [!TIP]
> Helpful advice for doing things better or more easily.

### Important

```
 > [!IMPORTANT]
 > Key information users need to know to achieve their goal.
```

> [!IMPORTANT]
> Key information users need to know to achieve their goal.

### Warning

```
 > [!WARNING]
 > Urgent info that needs immediate user attention to avoid problems.
```

> [!WARNING]
> Urgent info that needs immediate user attention to avoid problems.

### Caution

```
 > [!CAUTION]
 > Advises about risks or negative outcomes of certain actions.
 >
 > But multiline alerts can also be used.
```

> [!CAUTION]
> Advises about risks or negative outcomes of certain actions.
>
> But multiline alerts can also be used.
