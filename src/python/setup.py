from setuptools import find_packages, setup

package_name = 'python'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='zhuzeyu',
    maintainer_email='codepig_2278890271@163.com',
    description='TODO: Package description',
    license='TODO: License declaration',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
        'pub = python.publisher_node:main',
        'sub = python.subscriber_node:main',
        'turtle = python.turtle_control:main',
        ],
    },
)
