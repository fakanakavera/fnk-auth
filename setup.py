from setuptools import setup, find_packages

setup(
    name='fnk-auth',
    version='0.0.1.1',
    packages=find_packages(),
    include_package_data=True,
    description='A implementation of a robust and secure user authentication system for our application. This system will manage user identities, facilitate secure access to the application, and provide a seamless user experience for registration, login, and account management.',
    long_description=open('README.md').read(),
    url='https://github.com/fakanakavera/fnk-auth.git',
    author='FakaNaKavera',
    author_email='fakanakavera666@gmail.com',
    license='MIT',
    install_requires=[
        'Django>=3.0',
    ],
    classifiers=[
        'Framework :: Django',
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
