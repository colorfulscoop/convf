# convf

convf is a tool to filter and transform conversation data.

## Feature

* convf handles series of filters and transformations defined in a YAML configuration file which is readable and easy to reproduce the preprocessing.

## Installation

Install Python >= 3.8. Then install convf.

```sh
$ pip install git+https://github.com/colorfulscoop/convf
```

## Usage

convf provides a command line tool of `convf` .

Prepare conversation data with Json Line format.

```sh
$ head -n1000 test.jsonl  | python -m convf pipeline --config_file pipeline.yaml | jq
```

## Operation

| Name | Operation type |
| --- | --- |
| convf.FunctionFilter | FILTER |
| convf.MaxLenFilter | FILTER |
| convf.MinLenFilter | FILTER |
| convf.MaxTurnFilter | FILTER |
| convf.MinTurnFilter | FILTER |
| convf.DenyRegexFilter | FILTER |
| convf.FunctionTransform | TRANSFORM |
| convf.ReplaceTransform | TRANSFORM |
