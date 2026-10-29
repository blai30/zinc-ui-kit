from krita import Krita

from .extension import Capture

Krita.instance().addExtension(Capture(Krita.instance()))
