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

import zson

obj1 = zson.loads('  [ a\\\\b\\nc  : {\' x \':z  , "y":[aaa:bbb]},"c":  -0.123e-10  ,"d":[[{   }] ],"e":{},"f":false]')
print(obj1)
print(zson.dumps(obj1))
print(zson.loads(zson.dumps(obj1)))
print(obj1['a\\b\nc'])

obj2 = zson.loads('{a:{"a1","a2","a3"},a2:true,"a3":["a1","a2"],"a4":nulll,0:  null  ,"a5":"null"}')
print(obj2)
print(zson.dumps(obj2))
print(zson.loads(zson.dumps(obj2)))
print(obj2['a'])
