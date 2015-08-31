from setuptools import setup, find_packages

data_files = [
    ('share/doc/muzika', ['README.md'])
]

setup(
    name='muzika',
    version='1.1',
    description="Music Finder and Downloader",
    long_description=open('README.md').read(),
    author='Walid Saad',
    author_email='walid.sa3d@gmail.com',
    url='https://github.com/walidsa3d/muzika',
    # download_url='',
    license="GPL",
    keywords="music mp3 search download",
    packages=find_packages(),
    include_package_data=True,
    data_files=data_files,
    entry_points={"console_scripts": [""]},
    classifiers=[
    ]
)
