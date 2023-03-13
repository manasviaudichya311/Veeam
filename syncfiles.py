import argparse
import os
import shutil
from pathlib import Path
import time
import logging

parser = argparse.ArgumentParser(
					prog='Sync the folders',
					description='Sync source and destination folders',
					)

parser.add_argument('-s', '--source',required=True)
parser.add_argument('-d', '--destination',required=True)
parser.add_argument('-i', '--interval',required=True, help="input interval in seconds")
parser.add_argument('-l', '--logfilepath',required=True)

args = parser.parse_args()


source_path = os.path.abspath(args.source)
destination_path = os.path.abspath(args.destination)
interval = int(args.interval)
log_file_path = os.path.abspath(args.logfilepath)

# configure logging
logging.basicConfig(filename=log_file_path, encoding='utf-8', level=logging.INFO, format='%(asctime)s %(message)s')


def compare_directories(s, d):
	s_len = len(s.split(os.sep))
	d_len = len(d.split(os.sep))
	for root, _, files in os.walk(s):
		path = root.split(os.sep)
		
		# creating directories
		if s != os.path.abspath(root):
			s_path = Path(root)
			d_path = Path(d) / "/".join(path[s_len:])
			if not d_path.exists():
				print(f"creating folder at location: {d_path}")
				logging.info(f"creating folder at location: {d_path}")
				os.mkdir(d_path)
		
		# copying files
		for file in files:
			s_path = Path(root) / file
			d_path = Path(d) / "/".join(path[s_len:]) / file
			if not d_path.exists():
				print(f"copying file at location: {d_path}")
				logging.info(f"copying file at location: {d_path}")
				shutil.copy2(s_path, d_path)

	dirs_to_remove = []
	for root, _, files in os.walk(d):
		path = root.split(os.sep)
		
		# removing files
		for file in files:
			s_path = Path(root) / file
			d_path = Path(s) / "/".join(path[d_len:]) / file
			if not d_path.exists():
				print(f"removing the file at location: {s_path}")
				# logging.info(f"removing the file at location: {s_path}")
				os.remove(s_path)

		if d != os.path.abspath(root):
			s_path = Path(root)
			d_path = Path(s) / "/".join(path[d_len:])
			if not d_path.exists():
				dirs_to_remove.append(os.path.abspath(s_path).split(os.sep))

	
	dirs_to_remove = sorted(dirs_to_remove, reverse=True, key=len)
	for dir in dirs_to_remove:
		s_path = os.sep.join(dir)
		# removing directories
		print(f"removing the folder at location: {s_path}")
		logging.info(f"removing the folder at location: {s_path}")
		os.rmdir(s_path)

while True:
	compare_directories(source_path, destination_path)
	time.sleep(interval)