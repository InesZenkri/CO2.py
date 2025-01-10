from setuptools import setup, find_packages

setup(
    name='my_carbon_calculator',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests', 
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='A library for calculating carbon emissions and checking green domains.',
    url='https://github.com/ineszenkri/CO2.py',  
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)