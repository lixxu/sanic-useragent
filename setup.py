"""
sanic-useragent
--------------
Add `user_agent` to request for Sanic.
"""
from setuptools import setup

setup(
    name='sanic-useragent',
    version='0.1.2',
    url='https://github.com/lixxu/sanic-useragent',
    license='BSD',
    author='Lix Xu',
    author_email='xuzenglin@gmail.com',
    description='Add `user_agent` to request for Sanic.',
    long_description=__doc__,
    packages=['sanic_useragent'],
    zip_safe=False,
    platforms='any',
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ]
)
