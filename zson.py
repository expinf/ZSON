# -*- coding: utf-8 -*-
#
# Copyright (C) 2015 expinf <exp_inf@yahoo.com>
#
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

from collections import OrderedDict
import re

zson_to_python = {'null': None, 'true': True, 'false': False}
python_to_zson = {str(v): k for k, v in zson_to_python.items()}


encode_key = ['\\', '\t', '\r', '\n', '\f', '"']
encode_value = [r'\\', r'\t', r'\r', r'\n', r'\f', r'\"']
encode_dict = dict(zip(encode_key, encode_value))
encode_re = re.compile('|'.join(re.escape(c) for c in encode_key))

decode_key = encode_value + [r'\}', r'\]', r'\:', r'\,']
decode_value = encode_key + ['}', ']', ':', ',']
decode_dict = dict(zip(decode_key, decode_value))
decode_re = re.compile('|'.join(re.escape(c) for c in decode_key))


def encode(string):
	def encode_match(match):
		return encode_dict[match.group()]
	return encode_re.sub(encode_match, string)


def decode(string):
	def decode_match(match):
		return decode_dict[match.group()]
	return decode_re.sub(decode_match, string)


class ZSONDecoder:
	def __init__(self, s):
		self.i = 0
		self.s = s

	def consume(self, s):
		while self.i < len(self.s) and self.s[self.i] in set(' \t\r\n\f'):
			self.i += 1
		if self.i < len(self.s) and self.s[self.i] in set(s):
			self.i += 1
			return self.s[self.i - 1]

	def parse(self):
		result = self.parse_collection()
		if result is None:
			err, result = self.parse_null_or_num()
			if err:
				result = self.parse_str()
		return result

	def parse_collection(self):
		left = self.consume('{[')
		if left is not None:
			right = '}' if left == '{' else ']'
			self.consume('')
			if self.i < len(self.s) and self.s[self.i] == right:
				result = {} if left == '{' else []
			else:
				k = self.parse()
				if self.consume(':'):
					result = {} if left == '{' else OrderedDict()
					result[k] = self.parse()
					while self.consume(','):
						k = self.parse()
						self.consume(':')
						result[k] = self.parse()
				else:
					result = [k]
					while self.consume(','):
						result.append(self.parse())
					if left == '{':
						result = set(result)
			self.consume('}') if left == '{' else self.consume(']')
			return result

	def parse_null_or_num(self):
		self.consume('')
		left = self.i
		while self.i < len(self.s) and self.s[self.i] not in set(' \t\r\n\f"\'[{:,]}\\'):
			self.i += 1
		token = self.s[left:self.i]
		if token in zson_to_python:
			return False, zson_to_python[token]
		try:
			n = int(token)
		except:
			try:
				n = float(token)
			except:
				self.i = left
				return True, None
		return False, n

	def parse_str(self):
		quot = self.consume('"\'')
		special = quot if quot is not None else set(' \t\r\n\f:,]}')
		left = self.i
		escaped = False
		while self.i < len(self.s) and ((self.s[self.i] not in special) or escaped):
			if escaped:
				escaped = False
			elif self.s[self.i] == '\\':
				escaped = True
			self.i += 1
		string = self.s[left:self.i]
		if quot is not None:
			self.consume(quot)
		return decode(string)


def dumps(obj):
	if isinstance(obj, dict) or isinstance(obj, OrderedDict) or isinstance(obj, list) or isinstance(obj, set):
		if isinstance(obj, dict) or isinstance(obj, OrderedDict):
			strings = [dumps(k) + ': ' + dumps(v) for k, v in obj.items()]
		else:
			strings = [dumps(v) for v in obj]
		string = ', '.join(strings)
		return '[' + string + ']' if isinstance(obj, OrderedDict) or isinstance(obj, list) else '{' + string + '}'
	else:
		s = encode(str(obj))
		if obj is None or isinstance(obj, bool):
			return python_to_zson[s]
		elif isinstance(obj, int) or isinstance(obj, float):
			return s
		else:
			return '"' + s + '"'


def loads(s):
	return ZSONDecoder(s).parse()
