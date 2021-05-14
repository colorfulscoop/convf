import setuptools


setuptools.setup(
    name="convf",
    packages=setuptools.find_packages(),
    install_requires=[
        "fire>=0.4.0,<0.5",
        "envyaml>=1.0,<2.0",
    ],
    extras_require={
        "test": ["pytest>=5", "black==20.8b1"],
    },
    # If installing this script to the global name space, remove the folloing comment
    #entry_points={
    #    'console_scripts': ["convf=convf.__main__:entrypoint"]
    #},
    version="0.1.0",
    author="Colorful Scoop",

    # Description info
    url="https://github.com/colorfulscoop/convf",
    description=(
        "convf is a tool to filter and transform conversation data."
    ),
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",

    # Additional metadata
    classifiers=[
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ]
)
