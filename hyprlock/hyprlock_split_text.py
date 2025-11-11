#! /usr/bin/python

import sys
import unicodedata
import argparse
import re

parser = argparse.ArgumentParser(
                    prog='python hyperlock_split_text.py',
                    description='''This silly program just exists to split text\n
It will only split it into 2 lines, afterwhich it will start to shrink the text\n
 by using <span>. You can change the chars you consider break words (by default)\n
 only ' ' and '&', and the size of the box you want to fit it in.
''',)

parser.add_argument("-s","--separator", default="&", help="Defines the separators")
parser.add_argument("-S","--size", default=250, help="Defines the box's size")

args = parser.parse_args()

separator = args.separator
size = int(args.size)

string = sys.stdin.readline()

if len(string) > 25:
	string_split_index = len(string)//2
	
	regex = r"[{0}\s]+".format(separator)

	string_splits = re.split(regex, string)

	current_size=0

	for i in range(len(string_splits)):
		current_size+=len(string_splits[i])
		current_size+=1

		if current_size >= string_split_index and current_size < 1.5*string_split_index:
			break;
		elif current_size >= string_split_index*1.5:
			i-=1
			break;
	
	where_to_cut = len(" ".join(string_splits[:i+1]))
	first_string = string[:where_to_cut+1]
	second_string = string[where_to_cut+1:]

	if second_string[-1] == "\n":
		second_string = second_string[:-1]

	fs_width = sum(2 if unicodedata.east_asian_width(char) in 'FW' else 1 for char in first_string)*13.5 #11 is a very nice number I made up but it looks fine so it's fine :)
	ss_width = sum(2 if unicodedata.east_asian_width(char) in 'FW' else 1 for char in second_string)*13.5 #11 is a very nice number I made up but it looks fine so it's fine :)

	fs_size = (size*20)/fs_width;
	ss_size = (size*20)/ss_width; # I got this from a linear regression in libreoffice lol

	true_size = int(1024*min(fs_size, ss_size, 25)) #span's font_size works in 1024th of point

	print("<span font_size='{0}'>{1}\n{2}</span>".format(str(true_size),first_string,second_string))
	

else:
	print(string);


