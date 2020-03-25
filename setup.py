from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'h5py',
    'tables==3.5.2',
    'numpy==1.16.4',
    'pandas==0.24.0',
    'pandas-gbq==0.11.0',
    'scikit-learn==0.20.2'
]

setup(
    name='modeling',
    author='Renee Ernst',
    author_email='renee.ernst@genmills.com',
    version='0.0.2',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Test Job for GCP End to End Model Recommendations'
)
