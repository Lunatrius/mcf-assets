#!/usr/bin/env python2.7
import genbbcode
# mcfdata can be ommited, but I preffer to have that data on git,
# leaving out only the username and password
import mcfdata


def main():
    username = 'username'
    password = 'password'
    # read the comment in import section about mcfdata
    threads = mcfdata.threads('path/to/change/logs')

    genbbcode.genbbcode(username, password, threads)


if __name__ == '__main__':
    main()
