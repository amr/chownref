# -*- coding: utf-8 -*-

__version__ = "0.2.0"

import argparse
import os

from loggers import CompositeLogger, JsonLogger, TextLogger, NoOpLogger


class ChownReference:
	def __init__(self, dry_run, logger):
		self.dry_run = dry_run
		self.logger = logger

	def chown(self, src, dst):
		uid, gid = self._get_ownership(src)
		prev_uid, prev_gid = self._get_ownership(dst)

		if prev_uid == uid:
			uid = -1

		if prev_gid == gid:
			gid = -1

		if not self.dry_run and (uid != -1 or gid != -1):
			self._set_ownership(dst, uid, gid)

		if uid != -1 and gid != -1:
			self.logger.log_both_change(src, dst, uid, gid, prev_uid, prev_gid)
		elif uid != -1:
			self.logger.log_uid_change(src, dst, uid, gid, prev_uid, prev_gid)
		elif gid != -1:
			self.logger.log_gid_change(src, dst, uid, gid, prev_uid, prev_gid)
		else:
			self.logger.log_same(src, dst, uid, gid, prev_uid, prev_gid)

	def _get_ownership(self, path):
		"""Return a tuple of (uid, gid)"""
		stat = os.stat(path)
		return stat.st_uid, stat.st_gid

	def _set_ownership(self, path, uid, gid):
		os.chown(path, uid, gid)


def main():
	parser = argparse.ArgumentParser(description="Copy ownership and group between files, similar to chmod --reference")
	parser.add_argument('reference')
	parser.add_argument('target')
	parser.add_argument('--dry-run', '-d', help="Do not actually attempt to change anything, implies --verbose",
						default=False, action='store_true')
	parser.add_argument('--verbose', '-v', default=False, action='store_true', help="Logs all operations to standard output")
	parser.add_argument('--json', '-j', metavar='FILE', default=False, help="Write FILE with JSON formatted log of executed operations")

	args = parser.parse_args()

	if args.json and args.verbose:
		logger = CompositeLogger(JsonLogger(open(args.json, 'w')), TextLogger())
	elif args.json:
		logger = JsonLogger(open(args.json, 'w'))
	elif args.verbose or args.dry_run:
		logger = TextLogger()
	else:
		logger = NoOpLogger()

	try:
		ChownReference(args.dry_run, logger).chown(args.reference, args.target)
		logger.finalize()
	except OSError, e:
		parser.error(str(e))