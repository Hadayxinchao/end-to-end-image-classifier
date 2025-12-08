from setuptools import find_packages, setup

setup(
    name='image_classifier',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    python_requires='>=3.8',
    install_requires=[
        'torch>=2.0.0',
        'torchvision>=0.15.0',
        'numpy>=1.24.0',
        'scikit-learn>=1.3.0',
        'hydra-core>=1.3.0',
        'dvc>=3.0.0',
    ],
    author='Your Name',
    author_email='your.email@example.com',
    description='End-to-end image classifier with MLOps best practices',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/end-to-end-image-classifier',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
    ],
)
