from .main import Main


def entrypoint():
    import fire
    fire.Fire(Main)


if __name__ == "__main__":
    entrypoint()