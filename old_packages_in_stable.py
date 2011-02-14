#!/usr/bin/env python

import urllib2
import re

versions = ['5']
tags = ['stable']

for version in versions:
    for tag in tags:

        # IUS stable request
        req = urllib2.urlopen('http://dl.iuscommunity.org/pub/ius/' + tag + '/Redhat/' + version + '/SRPMS/')
        content = req.read()
        iuslinks = re.compile('<a href="(.*).src.rpm">').findall(content)

        filter = {}

        for package in iuslinks:
            split = package.split('-')
            list = []

            for num in range(3):
                match = re.compile('[a-z]').findall(split[num])
                if match and 'el5' not in split[num]:
                     list.append(split[num])
            list = '-'.join(list)
            filter[package] = list

old = {}
for package in sorted(filter):
    if filter.values().count(filter[package]) > 1:
        try:
            old[filter[package]]
        except:
            old[filter[package]] = package
        else:
            pass

print '='*35
print 'Old Packages in IUS Stable for EL5'
print '='*35
for package in sorted(old.values()):
    print package
print ' '

print '='*35
print 'Commands to archive:'
print '='*35
for package in sorted(old.values()):
    package = re.compile('(.*).el5').findall(package)
    print 'rpe-task untag', package[0], '-t stable'
    print 'rpe-task tag', package[0], '-t archive'
    print ' '
