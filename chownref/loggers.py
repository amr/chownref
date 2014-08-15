# -*- coding: utf-8 -*-

import logging
import json


class NoOpLogger:
	def __init__(self):
		pass

	def log_same(self, *args):
		pass

	def log_uid_change(self, *args):
		pass

	def log_gid_change(self, *args):
		pass

	def log_both_change(self, *args):
		pass

	def finalize(self):
		pass


class CompositeLogger:
	def __init__(self, *loggers):
		self.loggers = loggers

	def log_same(self, *args):
		for logger in self.loggers:
			logger.log_same(*args)

	def log_uid_change(self, *args):
		for logger in self.loggers:
			logger.log_uid_change(*args)

	def log_gid_change(self, *args):
		for logger in self.loggers:
			logger.log_gid_change(*args)

	def log_both_change(self, *args):
		for logger in self.loggers:
			logger.log_both_change(*args)

	def finalize(self):
		for logger in self.loggers:
			logger.finalize()


class TextLogger:
	def __init__(self):
		logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
		self.logger = logging

	def log(self, msg):
		self.logger.info(msg)

	def log_same(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.log("Same [uid=%s, gid=%s] found for [%s] and [%s]" % (prev_uid, prev_gid, dst, src))

	def log_uid_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.log("Changed UID for [%s] based on [%s] - [old_uid=%s, new_uid=%s]" % (dst, src, prev_uid, uid))

	def log_gid_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.log("Changed GID for [%s] based on [%s] - [old_gid=%s, new_gid=%s]" % (dst, src, prev_gid, gid))

	def log_both_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.log("Changed UID and GID for [%s] based on [%s] - [old_uid=%s, old_gid=%s, new_uid=%s, new_gid=%s]" % (dst, src, prev_uid, prev_gid, uid, gid))

	def finalize(self):
		pass


class JsonLogger:
	def __init__(self, logfile):
		self.logs = []
		self.logfile = logfile

	def log_same(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.logs.append({
			"src": src,
			"dst": dst,
			"changed": [],
			"prev": self._uid_gid(prev_uid, prev_gid),
			"new": self._uid_gid(uid, gid)
		})

	def log_uid_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.logs.append({
			"src": src,
			"dst": dst,
			"changed": ['uid'],
			"prev": self._uid_gid(prev_uid, prev_gid),
			"new": self._uid_gid(uid, gid)
		})

	def log_gid_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.logs.append({
			"src": src,
			"dst": dst,
			"changed": ['gid'],
			"prev": self._uid_gid(prev_uid, prev_gid),
			"new": self._uid_gid(uid, gid)
		})

	def log_both_change(self, src, dst, uid, gid, prev_uid, prev_gid):
		self.logs.append({
			"src": src,
			"dst": dst,
			"changed": ['uid', 'gid'],
			"prev": self._uid_gid(prev_uid, prev_gid),
			"new": self._uid_gid(uid, gid)
		})

	def finalize(self):
		self.logfile.write(json.dumps(self.logs))
		self.logfile.close()

	def _uid_gid(self, uid, gid):
		return {"uid": uid, "gid": gid}
