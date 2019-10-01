from setuptools import setup

setup(
    name='lpcdbeclient',
    version='0.1',
    description='Client for inferencing the LPC DBE',
    url='https://github.com/tklijnsma/lpcdbeclient.git',
    # download_url='https://github.com/tklijnsma/lpcdbeclient/archive/v0.tar.gz',
    author='Thomas Klijnsma',
    author_email='thomasklijnsma@gmail.com',
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
