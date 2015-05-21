#!/usr/bin/env python

# import packages
import sys, os, getopt

from distutils.util import strtobool

def prompt(query):
   sys.stdout.write('%s [y/n]: ' % query)
   val = raw_input()
   try:
       ret = strtobool(val)
   except ValueError:
       sys.stdout.write('Please answer with a y/n\n')
       return prompt(query)
   return ret

ROOT_DIR = '/var/www'

def usage():
    print('Usage:')
    print('\t{} [domain] -p\t\tCreate web directory structure for Python-based site.'.format(sys.argv[0]))
    print('\t{} [domain] -w\t\tCreate web directory structure for Wordpress-based site.'.format(sys.argv[0]))
    
if len(sys.argv) < 2:
    usage()
    sys.exit()

def main(argv):

    # defaults
    p_flag = True
    w_flag = False
    root_dir = ROOT_DIR

    # command-line arguments
    try:
        opts, args = getopt.gnu_getopt(argv, "hpwr:", ["help", "python","wordpress","root"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            usage()
            sys.exit()
        elif opt in ("-p", "--python"):
            p_flag = True
        elif opt in ("-w", "--wordpress"):
            w_flag = True
        elif opt in ("-r", "--root"):
            root_dir = arg
    domain = "".join(args)
    if 1 != sum([p_flag, w_flag]):
        sys.exit("Please supply exactly one option: -p or -w.")

    # construct commands
    cmds = []
    if p_flag:
        cmds.append("sudo mkdir -p {root}/{domain}/{{conf,logs,src,venv}}".format(root=root_dir,domain=domain))
    elif w_flag:
        cmds.append("sudo mkdir -p {root}/{domain}/{{public,private,logs,cgi-bin,backup}}".format(root=root_dir,domain=domain))
    else:
        sys.exit("Unsupported mode.")
    cmds.append("sudo chown -R www-data:www-data {root}/{domain}".format(root=root_dir,domain=domain))
    cmds.append("sudo chmod -R g+rw {root}/{domain}".format(root=root_dir,domain=domain))
    cmds.append("sudo find {root}/{domain} -type d -print0 | sudo xargs -0 chmod g+s".format(root=root_dir,domain=domain))
    cmds.append("sudo find {root}/{domain} -type d -exec chmod 2775 {{}} +".format(root=root_dir,domain=domain))
    cmds.append("sudo find {root}/{domain} -type f -exec chmod 0664 {{}} +".format(root=root_dir,domain=domain))

    # execute commands
    print("Domain: {}".format(domain))
    for c in cmds:
        print(c)
    if prompt("Execute these commands?"):
        for c in cmds:
            os.system(c)
    
    print("Program exited.")


if __name__ == "__main__":
    main(sys.argv[1:])
