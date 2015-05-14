from setuptools import setup, find_packages

setup(
    name='stacklog',
    version='0.1',
    description='Python timing and logging with nested data structures',
    url='http://github.com/ajfriend/stacklog',
    author='AJ Friend',
    author_email='ajfriend@stanford.edu',
    license='BSD',
    # packages=find_packages(),
    packages=['stacklog'],
    # List run-time dependencies here.  These will be installed by pip when
    # your project is installed. For an analysis of "install_requires" vs pip's
    # requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=[],

    # List additional groups of dependencies here (e.g. development
    # dependencies). You can install these using the following syntax,
    # for example:
    # $ pip install -e .[dev,test]
    extras_require={
        'dev': [],
        'test': ['nose'],
    },

)