import json
import numpy as np


class NumpyComplexArrayEncoder(json.JSONEncoder):
    def default(self, z):
        if isinstance(z, (np.ndarray, np.number)):
            return z.tolist()
        elif isinstance(z, (complex, np.complex)):
            return [z.real, z.imag]
        return json.JSONEncoder.default(self, z)
