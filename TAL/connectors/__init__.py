
import importlib

from . import exceptions 
from .. import settings

def import_connector(conf):
	modname = conf["connector"]
	try:
		mod = importlib.import_module("."+modname, package="TAL.connectors") # FIXME: Looks too dirty
	except ImportError, e:
		raise exceptions.ImproperlyConfigured("Error loading %s connector module: %s" % (modname, unicode(e)))

	mod.Connector.initialize(**conf["connector_options"])
	return mod.Connector

Connector = import_connector(settings.TAL)

