from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='supercanvas',
    version='0.6.1',
    description='tkinter simplified (and augmented) canvas',
    long_description_content_type='text/markdown',
    long_description=long_description,
    url='https://twitter.com/davidequantique',
    author='David COBAC',
    author_email='david.cobac@gmail.com',
    license='CC-BY-NC-SA',
    packages=find_packages(),
    python_requires='>3.2'
)
