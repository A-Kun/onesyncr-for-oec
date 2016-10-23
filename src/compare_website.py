'''
Created on Oct 16, 2016

@author: andrew
'''


from xml.etree.ElementTree import ElementTree
from xml.etree.ElementTree import Element
import xml.etree.ElementTree as etree

root=Element('date')
tree=ElementTree(root)
name=Element('name')
root.append(name)
name.text='text'
root.set('id','?')
print(etree.tostring(root))
