from setuptools import find_packages, setup

setup(
    name='textcount',
    version='0.1.0',
    description='Package for analyzing clipboard text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='text, clipboard, analyze, count',
    url='https://github.com/adamggrim/textcount',
    author='Adam Grim',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'nltk',
        'pyperclip',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'textcount=textcount.__main__:main'
        ]
    },
)