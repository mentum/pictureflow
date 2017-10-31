from setuptools import setup, find_packages
import re

version = ''
with open('pictureflow/__init__.py') as f:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', f.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Version is not set')

readme = 'See https://github.com/mentum/pictureflow for README.'

setup(
    name='pictureflow',
    author='mentum',
    author_email='dalloriam@gmail.com',
    url='https://github.com/mentum/pictureflow',
    version=version,
    packages=find_packages(),
    license='MIT',
    description='Image processing with a tensorflow-inspired API',
    long_description=readme,
    install_requires=[
        "numpy",
        "opencv-python==3.3.0.10"
    ]
)
