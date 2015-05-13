'''
Created on May 2, 2015

@author: PR0562
'''
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint

street_type_re = re.compile(r'\b\S+\.?$', re.IGNORECASE)


expected = ["Street", "Avenue", "Boulevard", "Drive", "Court", "Place", "Square", "Lane", "Road","Plaza", 
            "Trail", "Parkway", "Commons", "Terrace","Way","Path","Highway","Circle","Causeway","Highway","Grand Bay Drive South"]

mapping = { "St": "Street",
            "St.": "Street",
            "ave":"Avenue",
            "Ave":"Avenue",
            "Ave.":"Avenue",
            "Blvd":"Boulevard",
            "Cirlce":"Circle",
            "Ct":"Court",
            "Dr":"Drive",
            "Hwy":"Highway",
            "Rd":"Road",
            "Rd.":"Road",
            "St":"Street",
            "St.":"Street"
            }


def audit_street_type(street_types, street_name):
    m = street_type_re.search(street_name)
    if m:
        street_type = m.group()
        if street_type not in expected:
            street_types[street_type].add(street_name)


def is_street_name(elem):
    return (elem.attrib['k'] == "addr:street")


def audit(osmfile):
    osm_file = open(osmfile, "r")
    street_types = defaultdict(set)
    for event, elem in ET.iterparse(osm_file, events=("start",)):

        if elem.tag == "node" or elem.tag == "way":
            for tag in elem.iter("tag"):
                if is_street_name(tag):
                    audit_street_type(street_types, tag.attrib['v'])

    return street_types


def update_name(name, mapping):

    # YOUR CODE HERE
    keys=mapping.keys()
    for key in keys:
        name= re.sub(key+"$",mapping[key],name)
        
    return name

if __name__ == '__main__':
    st_types = audit("..\Miami.xml")
    pprint.pprint(dict(st_types))

    for st_type, ways in st_types.iteritems():
        for name in ways:
            better_name = update_name(name, mapping)
            print name, "=>", better_name
 