from install37 import setup
from vi37.__meta__ import __version__

if __name__ == "__main__":
    setup(
        name="vi37",
        version=__version__,
        author="Gabriel Amare", 
        author_email="gabriel.amare.dev@gmail.com",
        description="implementation of a modulable voice interface tool", 
        url="https://github.com/GabrielAmare/VoiceInterface", 
        packages=["vi37"], 
        classifiers=[], 
        python_requires=">=3.7"
    )
