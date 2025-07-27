from setuptools import setup, find_packages

setup(
    name='epacog',
    version='0.1.0',
    description='Recursive Epistemic Control under Drift, Rupture, and Collapse',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Pulikanti Sashi Bharadwaj',
    author_email='bharadwajpulikanti11@gmail.com',
    url='https://github.com/heraclitus0/epacog',
    packages=find_packages(),
    include_package_data=True,
    license='Apache-2.0',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Programming Language :: Python :: 3',
        'Operating System :: OS Independent',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
    ],
    install_requires=[
        'numpy>=1.20',
        'pandas>=1.3',
        'matplotlib>=3.4',
        'seaborn>=0.11'
    ],
    python_requires='>=3.8',
)
