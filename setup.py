from setuptools import setup, find_packages


setup(
    name="injson",
    version="0.1.0",
    author="Leo Tong",
    author_email="tonglei@qq.com",
    description="Test the sub json if or not in parent json",
    long_description=open("README.rst").read(),
    license="Apache License, Version 2.0",
    url="https://github.com/tonglei100/injson",
    #packages=['injson'],
    #package_data={'injson': ['*.py']},
    py_modules=['injson'],
    install_requires=[],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.6"
    ],
    entry_points={

    }
)
