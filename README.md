# convf

**convf** is a tool to filter and transform conversation data.

## Feature

* Handles series of filters and transformations defined in a YAML configuration file which is readable and easy to reproduce in the preprocessing stage.
* Easy to define your own filters and transformations

## Installation

Install Python >= 3.8. Then install convf.

```sh
$ pip install git+https://github.com/colorfulscoop/convf
```

## Tutorial

Let's move to the `example` directory for this tutorial.

```sh
$ cd example
```

### Data format

convf expects a [JSON Lines](https://jsonlines.org/) format data.  Each line needs to consist of an array of texts. Take a look at a sample JSON Line file of `sample.jsonl`.

```text
$ cat sample.jsonl
["Hi, how are you?", "Good!"]
["What's up?", "Not so bad. How about you?", "Fine, thanks!"]
["I am hungry.", "How about taking lunch first?", "That's a nice idea.", "And do exercise!"]
["mmm..."]
```

### Filter operation

For the first site, `["mmm..."]` should be removed for the conversation data because it only contains one utterance.
Take a look at how convf supports to remove the line. `filter.yaml` defined a **pipeline** to achieve this task.

```sh
$ cat filter.yaml
pipeline:
  - name: convf.MinTurnFilter
    params:
      min_turn: 2
```

Pipeline defines a series of **operations** . Operations can be categoreis into two types of **FILTER** and **TRANSFORM** .
**FILTER** is a operation to decide to filter out the line or not. On the other hand, **TRNASFORM** is a operation to update a line to new one.

Each operation in a pipeline needs to define two keys of `name` and `params`.
`name` requires a operation name. Each operation requires parameters which is given by the `params` key.

In the `filter.yaml` file, the pipeline deifnes one operation of **convf.MinTurnFilter** with the parameter of `min_turn` setting to `2`.
It means that it drops lines conversation turn of which is no more than 1.

Apply the pipeline to the file.

```sh
$ cat sample.jsonl | python -m convf pipeline --config_file filter.yaml
["Hi, how are you?", "Good!"]
["What's up?", "Not so bad. How about you?", "Fine, thanks!"]
["I am hungry.", "How about taking lunch first?", "That's a nice idea.", "And do exercise!"]
```

You can see that the line of `["mmm..."]` is removed in the output.

### Transform operation

For normalization purpose, try to replace `!` to `.` as a TRANFROM operation. `pipeline.yaml` defines the pipeline for this purpose.

```sh
$ cat pipeline.yaml
pipeline:
  - name: convf.MinTurnFilter
    params:
      min_turn: 2
  - name: convf.ReplaceTransform
    params:
      regex: "!"
      replacement: "."

```

As you can see in the piepeline, when several operations are defined in pipeline, each operation is applied from top to bottom of the definition.
For example, in this pipeline, `conv.MinTurnFilter` is first applied. Then `convf.ReplaceTransform` is applied.

`convf.ReplaceTransform` transform each utterance by replacing the text matched with the `regex` parameter with the `replacement` parameter.
Apply this pipeline.

```sh
$ cat sample.jsonl | python -m convf pipeline --config_file pipeline.yaml
["Hi, how are you?", "Good."]
["What's up?", "Not so bad. How about you?", "Fine, thanks."]
["I am hungry.", "How about taking lunch first?", "That's a nice idea.", "And do exercise."]
```

As you can see,

1. `["mmm..."]` was dropped by the first operation of `convf.MinTurnFilter`
2. All the appearance of `!` was replaced with `.` by the second operation of `conv.ReplaceTransform`

## Operation

The default operations defined in convf are as follows.

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

## How to define your own operation