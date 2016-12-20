import json
import numpy
class HelperJson(json.JSONEncoder):

    """
    commentaire a faire
    """
    def default(self,obj):
        if isinstance(obj, numpy.integer):
            return int(obj)
        elif isinstance(obj, numpy.floating):
            return float(obj)
        elif isinstance(obj, numpy.ndarray):
            return obj.tolist()
        else:
            return super(HelperJson, self).default(obj)
