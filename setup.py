from setuptools import setup


with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name='plisio',
    packages=['plisio'],
    version='1.0.8',
    license='MIT',
    description='Official Python SDK for Plisio API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Plisio',
    author_email='support@plisio.net',
    url='https://github.com/Plisio/plisio-python',
    download_url='https://github.com/Plisio/plisio-python',
    keywords=['plisio', 'crypto payment', 'sdk', 'bitcoin', 'etherium', 'crypto', 'blockchain'],
    install_requires=[
        'aiohttp',
        'requests',
        'hashlib',
        'hmac'
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
)
