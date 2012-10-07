from setuptools import setup, find_packages


setup(
    name='sqlalchemy-eav',
    version='0.1',
    py_modules=['eav'],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    url='',
    license='',
    author='Tomas Drencak',
    author_email='tomas@drencak.com',
    description='Generic Entity-Attribute-Value model for sqlalchemy',
    install_requires=['sqlalchemy'],
    test_suite='tests'
)
