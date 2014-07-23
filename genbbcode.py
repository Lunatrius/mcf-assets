#!/usr/bin/env python2.7
import sys
import json
import time
import mechanize
import subprocess
import cookielib


# update the thread
def genbbcode(username, password, threads=[]):
    # create a new browser
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # add user agent
    br.addheaders = [('User-agent', 'Mozilla/5.0 (Windows NT 6.3; Win64; x64; rv:3.6) Gecko/20100101 Firefox/3.6')]

    cj = cookielib.LWPCookieJar('cookies.txt')
    try:
        cj.load('cookies.txt')
    except Exception, e:
        pass
    cj.save('cookies.txt', ignore_discard=False, ignore_expires=False)
    br.set_cookiejar(cj)

    br.open('http://www.minecraftforum.net/')

    # save cookies
    cj.save('cookies.txt', ignore_discard=False, ignore_expires=False)

    loginlink = None
    for link in br.links():
        if ('id', 'login-link') in link.attrs:
            loginlink = link
            break

    if loginlink:
        print 'Trying to log in...'
        # open login form
        br.follow_link(link)

        # print the title of the window, just to make sure
        print '  Title: "%s"' % br.title()

        # inital form id
        frmid = 0

        # find the login form
        for frm in br.forms():
            if '/login?' in frm.action:
                break
            frmid += 1

        # select the form and fill in the username/password
        br.select_form(nr=frmid)
        br.form.find_control(id='field-username').value = username
        br.form.find_control(id='field-loginFormPassword').value = password

        # submit the form
        br.submit()

    # save cookies
    cj.save('cookies.txt', ignore_discard=False, ignore_expires=False)

    # for each thread
    for thread in threads:
        print 'Updating %s [%d]...' % (thread.get('title', 0), thread.get('t', 0))

        try:
            # open the thread edit page
            br.open('http://www.minecraftforum.net/comments/%d/edit' % (thread.get('p', 0)))

            # print the title of the window, just to make sure
            print '  Title: "%s"' % br.title()

            # inital form id
            frmid = 0

            # find the postingform id
            # for frm in br.forms():
            #     if frm.attrs['id'] == 'postingform':
            #         break
            #     frmid += 1

            # select the form and fill in the information
            br.select_form(nr=frmid)

            with open(thread.get('file', None), 'r') as fh:
                content = ''.join(fh.readlines())

                for key, value in thread.get('replacement', {}).items():
                    content = content.replace('%%%s%%' % (key), value)

                content = content.replace('<', '&lt;').replace('>', '&gt;')
                control = br.form.find_control(id='field-c%d-body-wysiwyg-bbcode' % (thread.get('p', 0)))

                control.value = content

            # submit the form
            response = br.submit(id='field-c%d-submit' % (thread.get('p', 0))).read()
            j = json.loads(response)
            print '  Response: %s' % (j['result'])
        except BaseException as e:
            print '  ERROR! %s' % (e)

    # save cookies
    cj.save('cookies.txt', ignore_discard=False, ignore_expires=False)

    p = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = p.communicate()
    stdout = data[0]

    # attempt to commit the changes
    if stdout.find('nothing to commit, working directory clean') == -1:
        print stdout
        if query_input('Would you like to commit the changes?', None) == True:
            p = subprocess.Popen(['git', 'add', '-A'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = p.communicate()

            p = subprocess.Popen(['git', 'diff', '--cached'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            data = p.communicate()
            stdout = data[0]

            print stdout

            if query_input('Would you really like to commit the changes?', None) == True:
                p = subprocess.Popen(['git', 'commit', '-m', '"Updated assets at %s"' % (time.strftime('%d.%m.%Y, %H:%M:%S'))], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                data = p.communicate()

                p = subprocess.Popen(['git', 'push'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                data = p.communicate()
                stdout = data[0]
                stderr = data[1]
                print stdout
                print stderr


# Modified version of: http://stackoverflow.com/questions/3041986/#3041990
def query_input(question, default=None):
    valid = {
        True: True,
        'true': True,
        'yes': True,
        'ye': True,
        'y': True,
        False: False,
        'false': False,
        'no': False,
        'n': False
    }

    if default == None:
        prompt = ' [y/n] '
    elif default == True:
        prompt = ' [Y/n] '
    elif default == False:
        prompt = ' [y/N] '
    else:
        raise ValueError('Invalid default answer: "%s"' % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
