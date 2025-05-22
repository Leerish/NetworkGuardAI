"""
Setup.py file is an essential part of packaging and distributing python projects. It is used 
by setup tools to define the configuration of the project like metadata , dependencies and more
"""

from setuptools import find_packages , setup 

"""
find_packages looks for packages .A package has __init__.py file
"""
from typing import List 

req_list: List[str] = []

def get_requirements()-> List:
    """
    This function returns List of requirements
    """
    try:
        with open('requirements.txt' , 'r') as file:
            #reads line 
            lines = file.readlines()
            # Process the lines 
            for line in lines:
                req = line.strip()
                ## Ignore empty lines and '-e .'
                if req and req != '-e .':
                    req_list.append(req)
    except FileNotFoundError:
        print("requirements.txt file not found")
        
    return req_list

setup(
    name = "NetworkSecurity",
    version = "0.0.1",
    author ="Leerish Arvind",
    author_email="leerisharvind@yahoo.com",
    packages= find_packages(),
    install_requires = get_requirements()
)


                