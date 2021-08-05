#!/home/hvianna/anaconda3/bin/python

'''

Your script you just need to make your script executable.
Something like chmod a+x [your-script].py should make it
executable and then you can just call ./[your-script.py]
in shell.

'''

from mellon_links import links_bny

urls = 'bny_urls'

if __name__ == "__main__":
    links_bny(name_output = urls)
