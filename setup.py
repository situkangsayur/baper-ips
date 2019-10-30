from setuptools import setup, find_packages

setup(
    name='baper-sis',

    version='1.0.0',


    author='Hendri',
    author_email='hendri@ieee.org',

    license='MIT',

    packages=find_packages(exclude=['tests']),

    install_requires=[
        'flask==1.0',
        'flask-mongoalchemy==0.7.2',
        'Flask-HTTPAuth==3.2.1',
        'Flask-WTF==0.13.1',
        'elasticsearch==2.4.0',
        'jsonmerge==1.2.1',
        'geopy==1.11.0',
        'scikit-learn==0.18.1',
        'Flask-PyMongo==0.3.1',
        'pymongo==2.8.1',
        'raven==5.32.0'
        # 'numpy==2.7.13'
    ]
)