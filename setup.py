from setuptools import find_packages, setup

setup(
    name="localtunnel-py",
    version="0.1.0",
    description="A Python client for Localtunnel.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="gweidart",
    author_email="gweidart@example.com",  # Add author email
    url="https://github.com/gweidart/localtunnel",  # Add project URL
    license="MIT",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Internet",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Internet :: Proxy Servers",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Software Development :: Build Tools",
        "Topic :: System :: Networking",
        "Topic :: System :: Networking :: Firewalls",
        "Topic :: Utilities",
        "Natural Language :: English",
        "Operating System :: OS Independent",
    ],  # Updated classifiers
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.11.2",
        "loguru>=0.7.2",
        "asyncio>=3.4.3",
        "nest_asyncio>=1.5.6",
    ],  # Updated dependencies
    entry_points={"console_scripts": ["lt=localtunnel.__main__:main"]},
    python_requires=">=3.12",
    project_urls={
        "Source": "https://github.com/gweidart/localtunnel",
        "Bug Tracker": "https://github.com/gweidart/localtunnel/issues",
    },
)
