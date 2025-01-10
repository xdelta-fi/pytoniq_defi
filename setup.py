import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pytoniq-defi",
    version="0.0.1",
    author="Nikos Papadopoulos",
    author_email="tonxdelta@proton.me",
    description="TON Blockchain DeFi TLB library",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages('.', exclude=['.idea', 'tests', 'examples', 'pytoniq_core/tlb/generator.py']),
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Software Development :: Libraries",
    ],
    url="https://github.com/xdelta-fi/pytoniq-defi",
    python_requires='>=3.9',
    py_modules=["pytoniq_defi"],
    install_requires=[
        "pytoniq_core>=0.1.36",
        "setuptools>=65.5.1"
    ]
)
