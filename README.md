## Synopsis
Kerrini is a free library of university-level material. All content is generated and reviewed by the users of the library.

## Motivation

A short description of the motivation behind the creation and maintenance of the project. This should explain **why** the project exists.

## Seting Up The environment
#### Make sure Python 3 is installed
You can verify that Python is installed by typing **python3** from your shell; you should see something like:

    Python 3.4.* (default, Nov 26 2013, 13:33:18)
    [GCC 4.8.2] on linux
    Type "help", "copyright", "credits" or "license" for more information.
    >>>

#### Install pip3:
On Ubuntu, simply run:

    sudo apt-get install python3-pip


#### Install Cassandra (make sure it's 2.1.11 that you're installing)
http://docs.datastax.com/en/cassandra/2.1/cassandra/install/installDeb_t.html


### Install Virtualenv and setup the environment

Virtulenv is a tool that allows you sandbox your python projects.
you can install packages directly in the sandbox without affecting your
global environment. To install virtualenv, just run

    sudo pip3 install virtualenv

once virtualenv is installed, choose a suitable directory name (for example ENV) and run

    virtualenv ENV

now to use the environment that you just created simply run the command

    source ENV/bin/activate

note that your shell prompt now starts with (ENV) which means that all your python commands that you
run on this current shell, will be the ones installed in this virtualenv.

    (ENV)yourprompt$



To deactivate the virtualenv you can simply run

    deactivate

### Make sure your virtualenv is activated before installing the following.

### Install Django:

    pip3 install django

### Verifying:

To verify that Django can be seen by Python, type **python3** from your shell. Then at the Python prompt, try to import Django:

    >>> import django
    >>> print(django.get_version())
    1.8


### Installing Cassandra driver for python

    pip3 install cassandra-driver

Refer to documentation on official datastax repostitory
https://github.com/datastax/python-driver

## Contributors

Simple rules to stick to really.
- Fork this repository to your github account.
- Once you're done with your work, make a pull request to me.
- Master branch should be ready for deployement at any given time. Therfore, make sure your code is tested before submitting a pull request.


## License

Not yet decided.
