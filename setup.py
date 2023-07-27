"""
sanic-useragent
--------------
Add `user_agent` to request for Sanic.
"""
from setuptools import setup

setup(
    name="sanic-useragent",
    version="0.1.4",
    url="https://github.com/lixxu/sanic-useragent",
    license="BSD",
    author="Lix Xu",
    author_email="xuzenglin@gmail.com",
    description="Add `user_agent` to request for Sanic.",
    long_description=__doc__,
    long_description_content_type="text/plain",
    packages=["sanic_useragent"],
    zip_safe=False,
    install_requires=["sanic>=20.6"],
    platforms="any",
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
