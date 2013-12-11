#!/usr/bin/env python
import sys
import time
import mechanize
import subprocess


# update the thread
def genbbcode(username, password, threads=[]):
    # create a new browser
    br = mechanize.Browser()
    br.set_handle_robots(False)

    # open login form
    br.open('http://www.minecraftforum.net/index.php?app=curseauth&module=global&section=login')

    # select the form and fill in the username/password
    br.select_form(nr=0)
    br.form['ips_username'] = username
    br.form['ips_password'] = password

    # submit the form
    br.submit()

    # for each thread
    for thread in threads:
        print 'Updating %s [%d]...' % (thread.get('title', 0), thread.get('t', 0))
        # open the thread edit page
        br.open('http://www.minecraftforum.net/index.php?app=forums&module=post&section=post&do=edit_post&f=%d&t=%d&p=%d&st=' % (thread.get('f', 0), thread.get('t', 0), thread.get('p', 0)))

        # print the title of the window, just to make sure
        print '  Title: "%s"' % br.title()

        # inital form id
        frmid = 0

        # find the postingform id
        for frm in br.forms():
            if frm.attrs['id'] == 'postingform':
                break
            frmid += 1

        # select the form and fill in the information
        br.select_form(nr=frmid)
        tag = thread.get('tag', None)
        title = thread.get('title', '')
        br.form['TopicTitle'] = '[%s] %s' % (tag, title) if tag and len(tag) > 0 else title
        br.form['ipsTags'] = ','.join(thread.get('tags', []))

        try:
            with open(thread.get('file', None), 'r') as fh:
                content = ''.join(fh.readlines())

                for key, value in thread.get('replacement', {}).items():
                    content = content.replace('%%%s%%' % (key), value)

                content = content.replace('<', '&lt;').replace('>', '&gt;')

                br.form['Post'] = content
        except BaseException as e:
            print 'ERROR! %s' % (e)

        # submit the form
        br.submit()

    p = subprocess.Popen(['git', 'status'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    data = p.communicate()
    stdout = data[0]

    # attempt to commit the changes
    if stdout.find('nothing to commit, working directory clean') == -1:
        print stdout
        if query_input('Would you like to commit the changes?', None) == True:
            p = subprocess.Popen(['git', 'add', '.'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
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
        "true": True,
        "yes": True,
        "ye": True,
        "y": True,
        False: False,
        "false": False,
        "no": False,
        "n": False
    }

    if default == None:
        prompt = " [y/n] "
    elif default == True:
        prompt = " [Y/n] "
    elif default == False:
        prompt = " [y/N] "
    else:
        raise ValueError("Invalid default answer: '%s'" % default)

    while True:
        sys.stdout.write(question + prompt)
        choice = raw_input().lower()
        if default is not None and choice == '':
            return valid[default]
        elif choice in valid:
            return valid[choice]
