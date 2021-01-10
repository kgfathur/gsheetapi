from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='gsheetapi',
    version='0.1.0',
    description='Sample Stuff for Implement Google Sheet API',
    long_description=readme,
    author='Fathur Rohman',
    author_email='kgfathur@gmail.com',
    url='https://github.com/kgfathur/gsheetapi',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)