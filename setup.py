from setuptools import setup, find_packages

setup(
    name='gmaps_avoid_swiss',
    version='0.1.11',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    url='https://github.com/xbencat/gmaps_avoid_swiss',
    license='MIT',
    author='Gregor Bencat',
    author_email='bencat.gregor@gmail.com',
    description='A Python package that customizes Google Maps routing to avoid Swiss routes.',
    install_requires=[
        'google-maps-routing~=0.6.8',
        'numpy~=1.21.2',
        'shapely~=1.6.0',
        'polyline~=1.4',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    package_data={
        '': ['data/*.geojson'],
    },
)
