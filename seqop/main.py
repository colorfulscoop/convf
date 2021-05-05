import json
import sys
from envyaml import EnvYAML
from .component import ComponentType


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
                component_type = component.get_component_type()

                # Change a behavior of each component based on its component type
                if component_type == ComponentType.FILTER:
                    if not component(conv):
                        filter_result = False
                        break
                elif component_type == ComponentType.TRANSFORM:
                    conv = component(conv)
                else:
                    raise Exception(
                        f"Component type of {component_type} "
                        f"for {component.__class__.__name__} "
                        f"should be one of [{ComponentType.FILTER}, {ComponentType.TRANSFORM}]"
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