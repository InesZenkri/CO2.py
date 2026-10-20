from setuptools import setup, find_packages

setup(
    name='CO2.py',
    version='0.2.0',
    packages=find_packages(),
    install_requires=[],
    author='Ines',
    description='Estimate carbon emissions of internet data transfer (Sustainable Web Design Model v4) and check green hosting.',
    url='https://github.com/InesZenkri/CO2.py',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.9',
)
