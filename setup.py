from setuptools import setup

setup(
    name='trainSearch',
    version='1',
    packages=['api', 'logs', 'tests', 'batch_jobs', 'exceptionhandling'],
    url='',
    license='',
    author='xelmagax',
    author_email='riccardo.maganza@gmail.com',
    description='Gets train info from Viaggiatreno in real time using Kafka and saves to MongoDB',
    install_requires=['holidays', 'yagmail']
)
