from urllib import unquote
from xml.dom.minidom import parse
import re

from utils.objects import AbstractUserObject

class BMML(object):
    def __init__(self, path):
        self.path = path
        self.dom = parse(path)
        self.forms = self._find_forms()

    def _find_forms(self):
        groups = []
        for control in self.dom.getElementsByTagName('control'):
            if '__group__' == control.getAttribute('controlTypeID'):
                groups.append(Form(self, control))
        return groups

    def find_form(self, name):
        for form in self.forms:
            if form.name == name:
                return form

class Control(object):
    def __init__(self, controlID, controlTypeID, x, y, w, h, measuredW, measuredH, zOrder, locked, isInGroup):
        self.controlID = controlID
        self.controlTypeID = controlTypeID
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.measuredW = measuredW
        self.measuredH = measuredH
        self.zOrder = zOrder
        self.locked = locked
        self.isInGroup = isInGroup

    def __repr__(self):
        return self.__unicode__()

    def __unicode__(self):
        return unicode('<control controlID="%s" controlTypeID="%s" x="%s" y="%s" w="%s" h="%s" measuredW="%s" measuredH="%s" zOrder="%s" locked="%s" isInGroup="%s">' % (self.controlID, self.controlTypeID, self.x, self.y, self.w, self.h, self.measuredW, self.measuredH, self.zOrder, self.locked, self.isInGroup))

CONTROL_VALIDATOR = re.compile(r'^(com.balsamiq.mockups::|__group__$)')

class Form(object, AbstractUserObject):

    @staticmethod
    def from_json(name, path):
        return BMML(path).find_form(name)

    def __init__(self, bmml, dom):
        self.bmml = bmml
        self.dom = dom
        try:
            self.name = dom.getElementsByTagName('controlName')[0].childNodes[0].nodeValue
            self.name = unquote(self.name)
        except IndexError:
            # There was an error trying to retrieve the name so it has no name
            print('file "%s" contains an un-named group.  All groups must have a name' % self.bmml.path)
            sys.exit(1)
        self.controls = self._build_controls()

    def _build_controls(self):
        built_controls = []
        children_descriptors = self.dom.getElementsByTagName('groupChildrenDescriptors')[0]
        for c in children_descriptors.getElementsByTagName('control'):
            if CONTROL_VALIDATOR.match(c.getAttribute('controlTypeID'))== None:
                continue
	    one_built_control = Control(c.getAttribute('controlID'),
                                        c.getAttribute('controlTypeID'), 
                                        c.getAttribute('x'), 
                                        c.getAttribute('y'),
                                        c.getAttribute('w'), 
                                        c.getAttribute('h'), 
                                        c.getAttribute('measuredW'),
                                        c.getAttribute('measuredH'), 
                                        c.getAttribute('zOrder'),
                                        c.getAttribute('locked'),
                                        c.getAttribute('isInGroup'))
            built_controls.append(one_built_control)
        return built_controls

    def _json_encode(self):
        return {'py/object': 'forms.Form', 'name': str(self.name), 'path': str(self.bmml.path)}

    def __unicode__(self):
        output_string_list = [self.name]
        for c in self.controls:
            output_string_list.append(u'\n|--%s' % c.controlTypeID)
        return unicode(''.join(output_string_list))

    def __repr__(self):
        return self.__unicode__()

