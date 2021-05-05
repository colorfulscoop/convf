# seqop

seqop is a **seq**uence **op**eration tool to filter and transform text sequence data.

ConvKit provides tools to support preprocessing conversation data.

## Feature

* Easy to understand your pipeline
* Easy to manage reproducibility

## Installation

Install Python >= 3.8. Then install seqop.

```sh
$ pip install git+https://github.com/colorfulscoop/seqop
```

## Usage

seqop provides a command line tool of `seqop` .

Prepare conversation data with Json Line format.

```
head -n1000 test.jsonl  | seqop pipeline --config_file pipeline.yaml
```