from setuptools import setup

setup(
    name='lpcdbeclient',
    version='0.1',
    license='BSD 3-Clause License',
    description='Client for inferencing the LPC DBE',
    url='https://github.com/tklijnsma/lpcdbeclient.git',
    download_url='https://github.com/tklijnsma/lpcdbeclient/archive/v0_1.tar.gz',
    author='Thomas Klijnsma',
    author_email='tklijnsm@gmail.com',
    packages=['lpcdbeclient'],
    zip_safe=False,
    tests_require=['nose'],
    test_suite='nose.collector',
    scripts=[
        'bin/lpcdbe-run',
        'bin/lpcdbe-run-test',
        'bin/lpcdbe-deploymodule',
        ],
    )
