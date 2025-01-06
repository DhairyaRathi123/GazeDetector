from setuptools import setup, find_packages

setup(
    name='gazedetector',  # Name of your package
    version='1.0',      # Package version
    packages=find_packages(),  # Automatically find all the packages in the directory
    author='Dhairya Rathi',   # Specify the author's name
    author_email='Drdhairya12@outlook.com',  # Specify the author's email
    description='A Python package for gaze detection integration in web apps',  # Short description
    long_description=open('README.md').read(),  # Read long description from README file
    long_description_content_type='text/markdown',  # Specify the content type for long description
    url='https://github.com/DhairyaRathi123/GazeDetectorr',  # URL for the project (e.g., GitHub repo)
    classifiers=[         # Optional classifiers that help categorize your project
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    install_requires=[     # List of dependencies
        'flask',
        'opencv-python',
        # add any other dependencies here
    ],
    python_requires='>=3.6',  # Minimum Python version required
)
