from setuptools import setup

setup(
    name="gesture-music-player",
    version="1.0.0",
    python_requires=">=3.8,<3.12",
    install_requires=[
        "opencv-python>=4.8.0",
        "mediapipe>=0.10.0",
        "pygame>=2.1.0"
    ]
)

