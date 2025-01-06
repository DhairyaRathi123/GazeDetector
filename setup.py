from setuptools import setup, find_packages

setup(
    name='gazedetector',
    version='0.5.0',
    packages=find_packages(),
    install_requires=[
        'Flask',
        'mediapipe',
        'opencv-python'
    ],
    include_package_data=True,
    package_data={
        'gazedetector': ['static/index.html'],
    },
    entry_points={
        'console_scripts': [
            'gazedetector=gazedetector.gaze_detector:run_server',
        ],
    },
)
