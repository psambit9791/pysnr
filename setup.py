from setuptools import setup, find_packages

setup(
    name='pysnr',
    version='0.0.1',
    url='https://github.com/psambit9791/pysnr',
    license='MIT',
    author='Sambit Paul',
    author_email='sambitpaul1992@gmail.com',
    description='Computing Signal-to-Noise Ratio based on MATLAB implementation',
    packages=find_packages(),
    install_requires=['numpy==1.22.4', 'scipy==1.8.1']
)
