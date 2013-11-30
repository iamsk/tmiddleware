import os
from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='TMiddleware',
    version='0.0.1',
    description='tornado middleware',
    long_description=read('README.md'),
    author='iamsk',
    author_email='iamsk.info@gmail.com',
    url='https://github.com/iamsk/tmiddleware',
    packages=find_packages(exclude=('examples', 'tests')),
    install_requires=[
        'tornado>=2.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Framework :: Tornado',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
    ],
    include_package_data=True,
    zip_safe=False,
)
