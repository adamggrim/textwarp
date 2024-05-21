from setuptools import find_packages, setup

setup(
    name='textwarp',
    version='0.5',
    description='Package for manipulating clipboard text',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords='text, clipboard, text manipulation',
    url='https://github.com/adamggrim/textwarp',
    author='Adam Grim',
    license='MIT',
    packages=find_packages(),
    install_requires=[
        'pyperclip',
        'setuptools'
    ],
    entry_points={
        'console_scripts': [
            'textwarp=textwarp.__main__:main'
        ]
    },
)