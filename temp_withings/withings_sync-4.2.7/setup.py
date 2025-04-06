import os
import sys
from setuptools import setup, find_packages

def read(fname):
    """Read a file's contents as a string."""
    try:
        # Try to get the absolute path first
        abs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), fname))
        
        # Try different encoding approaches
        encodings = ['utf-8', 'cp950', 'gbk', sys.getfilesystemencoding()]
        
        for encoding in encodings:
            try:
                with open(abs_path, encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except FileNotFoundError:
                continue
        
        # If all encodings fail, try binary read
        with open(abs_path, 'rb') as f:
            return f.read().decode('utf-8', errors='ignore')
    except Exception as e:
        # If all attempts fail, return a minimal description
        print(f"Warning: Could not read {fname}: {str(e)}")
        return "A Python library for synchronizing health data"

setup(
    name="withings-sync",
    version="4.2.7",
    author="Masayuki Takagi",
    author_email="kamonama@gmail.com",
    description="A Python library for synchronizing health data",
    long_description=read("README.md"),
    long_description_content_type="text/markdown",
    license="MIT",
    keywords="withings health sync",
    url="https://github.com/matin/withings-sync",
    packages=find_packages(),
    install_requires=[
        "lxml>=4.9.0",
        "requests>=2.28.0"
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    python_requires=">=3.7",
) 