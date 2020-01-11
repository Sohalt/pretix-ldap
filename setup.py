import os
from setuptools import setup, find_packages


try:
    with open(os.path.join(os.path.dirname(__file__), 'README.rst'), encoding='utf-8') as f:
        long_description = f.read()
except:
    long_description = ''


setup(
    name='pretix-ldap',
    version='0.0.2',
    description='LDAP authentication backend for pretix',
    long_description=long_description,
    url='https://github.com/Sohalt/pretix-ldap',
    author='sohalt',
    author_email='sohalt@sohalt.net',
    license='Apache Software License',

    install_requires=['ldap3'],
    packages=find_packages(exclude=['tests', 'tests.*']),
    include_package_data=True,
    entry_points="""
[pretix.plugin]
pretix_ldap=pretix_ldap:PretixPluginMeta
""",
)
