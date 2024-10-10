from setuptools import setup, find_packages

setup(
    name='custom_debugger',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ipdb'
    ],
    author='Emrys-hong',
    author_email='hongpengfei.emrys@gmail.com',
    description='debugger work for both torch and normal use',
    long_description=open('readme.md').read(),
    long_description_content_type='text/markdown'
)
