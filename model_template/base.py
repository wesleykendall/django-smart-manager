from copy import deepcopy

from manager_utils import upsert


class BaseModelTemplate(object):
    def __init__(self, template):
        self._template = deepcopy(template)
        self._built_objs = set()

    @property
    def built_objs(self):
        return self._built_objs

    def build_obj(self, model_class, updates=None, defaults=None, **kwargs):
        """
        Builds an object using the upsert function in manager utils. All
        built objects are added to the internal _built_objs list and returned.
        """
        built_obj = upsert(model_class.objects, updates=updates, defaults=defaults, **kwargs)[0]
        self._built_objs |= set([built_obj])

        return built_obj

    def build_obj_using(self, model_template_class, template):
        """
        Builds objects using another builder and a template. Adds the resulting built objects
        from that builder to the built objects of this builder.
        """
        model_template = model_template_class(template)
        built_obj = model_template.build()
        self._built_objs |= model_template.built_objs

        return built_obj

    def build(self):
        """
        All builders must implement the build function, which returns the built object. All build
        functions must also maintain an interal list of built objects, which are accessed by
        self.built_objs.
        """
        raise NotImplementedError