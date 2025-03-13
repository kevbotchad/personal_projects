from setuptools import setup, find_packages

setup(
    name="nexussre",
    version="0.1.0",
    description="A Python client for interacting with the Nexus Sonatype API",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/nexus-sonatype",
    author="Your Name",
    author_email="youremail@example.com",
    license="MIT",
    packages=find_packages(),
    install_requires=['requests','PyYAML','urllib3', 'twine'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12.8",
)
