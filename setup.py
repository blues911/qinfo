from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name='qinfo',
    version='0.1',
    description='Linux system info',
    long_description=readme(),
    url='https://github.com/smokehill/qinfo',
    author='Valera Padolochniy',
    author_email='valera.padolochniy@gmail.com',
    license='MIT',
    packages=['qinfo'],
    entry_points={
        'console_scripts': ['qinfo=qinfo.main:main'],
    },
    classifiers=[
        'Environment :: Console',
        'License :: OSI Approved :: MIT',
        'Programming Language :: Python :: 2.7',
    ],
)