#!/home/hvianna/anaconda3/bin/python

'''

Your script you just need to make your script executable.
Something like chmod a+x [your-script].py should make it
executable and then you can just call ./[your-script.py]
in shell.

'''

import os

from cont_df import jdf
from mellon_links import links_bny
from nav_info import get_nav
from yesterday import show_yday

urls = 'bny_urls.xlsx'
finput = 'my_input.xlsx'
calendar_file = 'ANBIMA.txt'

if __name__ == "__main__":
    double_check = os.path.isfile(urls)

    if double_check == False:
        links_bny(name_output=urls)

    if double_check == True:
        my_yesterday = show_yday(calendar_file)
        print(my_yesterday)

        # pre_df = jdf(bny_file=urls, user_file=finput)
        # final_dataframe = get_nav(tg_dataframe=pre_df)
        #
        # final_dataframe.to_excel('TEMP', index=False)
