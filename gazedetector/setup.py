from setuptools import setup, find_packages

setup(
    name='gazedetector',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flask',
        'flask-cors',
        'opencv-python-headless',
    ],
    entry_points={
        'console_scripts': [
            'gazedetector = gazedetector.server:run_server',
        ],
    },
)
