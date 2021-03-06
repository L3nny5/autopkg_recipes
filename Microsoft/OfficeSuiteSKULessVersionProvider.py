#!/usr/bin/env python
#
# Copyright 2016 Allister Banks, lovingly based on work by Hannes Juutilainen
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import urllib2
import xml.etree.ElementTree as ET

from autopkglib import Processor, ProcessorError


__all__ = ["OfficeSuiteSKULessVersionProvider"]


class OfficeSuiteSKULessVersionProvider(Processor):
    """Provides the version of the latest SKU-Less Office 2016 Suite release"""
    input_variables = {
        "feed_url": {
            "required": True,
            "description": (
                "URL to parse")
        },
        "versionid": {
            "required": True,
            "description": (
                "ID of FEED_URL which product to download")
        },
    }
    output_variables = {
        "version": {
            "description": "Version of the latest SKU-Less Office release.",
        },
        "downloadurl": {
            "description": "Output Download URL to use from FEED_URL",
        }
    }
    description = __doc__

    def get_version(self, FEED_URL):
        """Parse the FEED_URL feed for the latest version number"""
        try:
            raw_xml = urllib2.urlopen(FEED_URL)
            xml = raw_xml.read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

        root = ET.fromstring(xml)
        latest = root.find('latest')
        versionid = self.env["versionid"]
        for vers in root.iter('latest'):
            package = vers.find('package')
            for pack in vers.iter('package'):
                if pack.find('id').text == versionid:
                    version = pack.find('version').text.split(" ")[0]
        return version

    def get_downlink(self, FEED_URL):
        try:
            raw_xml = urllib2.urlopen(FEED_URL)
            xml = raw_xml.read()
        except BaseException as e:
            raise ProcessorError("Can't download %s: %s" % (FEED_URL, e))

        root = ET.fromstring(xml)
        latest = root.find('latest')
        versionid = self.env["versionid"]
        for vers in root.iter('latest'):
            package = vers.find('package')
            for pack in vers.iter('package'):
                if pack.find('id').text == versionid:
                    downurl = pack.find('download').text
        return downurl

    def main(self):
        FEED_URL = self.env["feed_url"]
        self.env["version"] = self.get_version(FEED_URL)
        self.env["downloadurl"] = self.get_downlink(FEED_URL)
        self.output("Found Version Number %s" % self.env["version"])
        self.output("Found Download URL %s" % self.env["downloadurl"])


if __name__ == "__main__":
    processor = OfficeSuiteSKULessVersionProvider()
    processor.execute_shell()
