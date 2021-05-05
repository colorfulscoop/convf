import json
import sys
from envyaml import EnvYAML
from .operation import OperationType


def load_module(name: str):
    components = name.split(".")
    mod = __import__(".".join(components[:-1]), fromlist=[components[-1]])
    return getattr(mod, components[-1])


class Main:
    def operation(self):
        raise NotImplemented()

    def pipeline(self, config_file):
        config = EnvYAML(config_file, include_environment=False).export()

        # build pipeline
        pipeline = config["pipeline"]
        pipeline = [load_module(item["name"])(**item["params"]) for item in pipeline]

        for line in sys.stdin:
            line = line.rstrip("\n")
            conv = json.loads(line)

            filter_result = True

            for component in pipeline:
                op_type = component.get_operation_type()

                # Change a behavior of each component based on its component type
                if op_type == OperationType.FILTER:
                    if not component(conv):
                        filter_result = False
                        break
                elif op_type == OperationType.TRANSFORM:
                    conv = component(conv)
                else:
                    raise Exception(
                        f"Component type of {op_type} "
                        f"for {component.__class__.__name__} "
                        f"should be one of [{OperationType.FILTER}, {OperationType.TRANSFORM}]"
                    )

            if not filter_result:
                continue

            # Transforms

            # Show result
            res = json.dumps(conv)
            print(res)


def entrypoint():
    import fire
    fire.Fire(Main)


if __name__ == "__main__":
    entrypoint()