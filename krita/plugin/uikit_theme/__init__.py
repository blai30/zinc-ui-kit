from krita import Krita

from .extension import UIKitExtension

Krita.instance().addExtension(UIKitExtension(Krita.instance()))
