from setuptools import find_packages
from setuptools import setup

REQUIRED_PACKAGES = [
    'h5py',
    'tables',
    'numpy',
    'pandas',
    'pandas-gbq',
    'scikit-learn==0.20.4'
]

setup(
    name='modeling',
    author='Renee Ernst',
    author_email='renee.ernst@genmills.com',
    version='0.0.1',
    install_requires=REQUIRED_PACKAGES,
    packages=find_packages(),
    include_package_data=True,
    description='Test Job for GCP End to End Model Recommendations'
)
