import pathlib

from setuptools import find_packages, setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()

setup(
    name="EasIlastik",
    version="1.0.2",
    author="Titouan Le Gourrierec",
    author_email="titouanlegourrierec@icloud.com",
    url="https://github.com/titouanlegourrierec/EasIlastik",
    long_description=README,
    long_description_content_type="text/markdown",
    description="This package provides seamless integration of pre-trained image segmentation models from Ilastik into Python workflows, empowering users with efficient and intuitive image segmentation capabilities for diverse applications.",
    packages=find_packages(),
    install_requires=[
        "h5py",
        "numpy",
        "opencv-python",
        "requests",
    ],
    python_requires=">=3.9",
    classifiers=[
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Operating System :: OS Independent",
        "Intended Audience :: Science/Research",
    ],
    license="GPLv3",
    keywords="ilastik image-segmentation machine-learning python image",
)
