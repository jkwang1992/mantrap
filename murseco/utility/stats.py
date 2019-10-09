from abc import abstractmethod
from typing import Any, Dict, Union

import numpy as np

from murseco.utility.io import JSONSerializer


class Distribution2D(JSONSerializer):
    def __init__(self, name):
        super(Distribution2D, self).__init__(name)

    @abstractmethod
    def pdf_at(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> Union[None, np.ndarray]:
        """Get probability density function value at given location(s).
        The x, y coordinates can either be single coordinates or larger matrices, the function is shape containing,
        i.e. it returns probability values with the same shape as x and y (MxN). Since the evaluation of the pdf
        function is based on (x, y) pairs hence x and y have to be in the same shape.

        :argument x: array of x points to evaluate (MxN).
        :argument y: array of y points to evaluate (MxN).
        :return pdf values for given (x,y)-pairs (MxN).
        """
        x, y = np.asarray(x), np.asarray(y)
        assert x.shape == y.shape, "x and y have to be in the same shape to compute pdf-values"
        return None

    @abstractmethod
    def sample(self, num_samples: int) -> np.ndarray:
        """Sample N = num_samples from distribution and return results stacked in array.

        :argument num_samples: number of samples to return.
        :return 2D samples array (num_samples x 2).
        """
        pass


class Point2D(Distribution2D):
    """f(x) = direc_delta(x) with x = point (direc_delta is modelled with np.inf)"""

    def __init__(self, position: np.ndarray):
        super(Point2D, self).__init__("utility/stats/Point2D")

        assert position.size == 2, "position must be two-dimensional"
        self.x, self.y = position.tolist()

    def pdf_at(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> Union[None, np.ndarray]:
        super(Point2D, self).pdf_at(x, y)
        mask = np.logical_and(np.isclose(self.x, x, rtol=0.01), np.isclose(self.y, y, rtol=0.01)).astype(int)
        if np.amax(mask) == 0:
            return np.zeros_like(x)
        else:
            return mask * np.inf

    def sample(self, num_samples: int) -> np.ndarray:
        raise NotImplementedError

    def summary(self) -> Dict[str, Any]:
        summary = super(Point2D, self).summary()
        summary.update({"point": [self.x, self.y]})
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        super(Point2D, cls).from_summary(json_text)
        return cls(np.asarray(json_text["point"]))


class Static2D(Distribution2D):
    """f(x) = 1 for all x within the rectangular borders, 0 otherwise (not a real probability function)"""

    def __init__(self, borders: np.ndarray):
        super(Static2D, self).__init__("utility/stats/Static2D")

        assert borders.size == 4, "block array has to be in form (x_min, x_max, y_min, y_max)"
        assert borders[0] < borders[1], "x_max has to be a larger value than x_min"
        assert borders[2] < borders[3], "y_max has to be a larger value than y_min"

        self.x_min, self.x_max, self.y_min, self.y_max = borders.tolist()

    def pdf_at(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> Union[None, np.ndarray]:
        super(Static2D, self).pdf_at(x, y)
        mask = np.logical_and(
            np.logical_and(self.x_min <= x, x <= self.x_max), np.logical_and(self.y_min <= y, y <= self.y_max)
        )
        return np.asarray(np.ones_like(x) * mask, dtype=float)

    def sample(self, num_samples: int) -> np.ndarray:
        raise NotImplementedError

    def summary(self) -> Dict[str, Any]:
        summary = super(Static2D, self).summary()
        summary.update({"borders": [self.x_min, self.x_max, self.y_min, self.y_max]})
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        super(Static2D, cls).from_summary(json_text)
        return cls(np.asarray(json_text["borders"]))


class Gaussian2D(Distribution2D):
    """f(x) = 1 / /sqrt(2*pi )^p * det(Sigma)) * exp(-0.5 * (x - mu)^T * Sigma^(-1) * (x - mu))"""

    def __init__(self, mu: np.ndarray, sigma: np.ndarray):
        super(Gaussian2D, self).__init__("utility/stats/Gaussian2D")
        mu, sigma = np.squeeze(mu), np.squeeze(sigma)  # prevent e.g. sigma.shape = (1, 2, 2)

        assert mu.size == 2, "mean vector has to be two dimensional"
        assert sigma.shape == (2, 2), "variance matrix has to be two-by-two"
        assert np.linalg.det(sigma) != 0, "variance matrix has to be invertible"
        assert sigma[0, 1] == sigma[1, 0], "variance matrix has to be symmetric"

        self._K1 = 1 / (2 * np.pi * np.sqrt(np.linalg.det(sigma)))
        self._K2 = -0.5 / (sigma[0, 0] * sigma[1, 1] - sigma[0, 1] ** 2)
        self.mu, self.sigma = mu, sigma

    def pdf_at(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> Union[None, np.ndarray]:
        super(Gaussian2D, self).pdf_at(x, y)
        dx, dy = x - self.mu[0], y - self.mu[1]
        sx, sy, sxy = self.sigma[0, 0], self.sigma[1, 1], self.sigma[0, 1]
        return self._K1 * np.exp(self._K2 * (dx ** 2 * sy - 2 * sxy * dx * dy + dy ** 2 * sx))

    def sample(self, num_samples: int) -> np.ndarray:
        super(Gaussian2D, self).sample(num_samples)
        return np.random.multivariate_normal(self.mu, self.sigma, size=num_samples)

    def summary(self) -> Dict[str, Any]:
        summary = super(Gaussian2D, self).summary()
        summary.update({"mu": self.mu.tolist(), "sigma": self.sigma.tolist()})
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        super(Gaussian2D, cls).from_summary(json_text)
        mu = np.asarray(json_text["mu"])
        sigma = np.reshape(np.asarray(json_text["sigma"]), (2, 2))
        return cls(mu, sigma)


class GMM2D(Distribution2D):
    """f(x) = sum_i w_i * Gaussian2D_i(x)"""

    def __init__(self, mus: np.ndarray, sigmas: np.ndarray, weights: np.ndarray):
        super(GMM2D, self).__init__("utility/stats/GMM2D")
        mus = mus.squeeze() if len(mus.shape) > 2 else mus  # prevent e.g. mus.shape = (1, 4, 2) but (1, 2)
        sigmas = sigmas.squeeze() if len(sigmas.shape) > 3 else sigmas
        weights = weights.squeeze() if len(weights.shape) > 1 else weights

        assert len(mus.shape) == 2, "mus must be a stack of two-dimensional vectors"
        assert len(sigmas.shape) == 3, "sigmas must be a stack of 2x2 matrices"
        assert mus.shape[0] == sigmas.shape[0], "length of mus and sigmas array must be equal"
        assert mus.shape[0] == weights.size, "length of gaussians and weights must be equal"

        self.num_modes = mus.shape[0]
        self.gaussians = [Gaussian2D(mus[i, :], sigmas[i, :, :]) for i in range(self.num_modes)]
        self.weights = weights / np.sum(weights)  # from now on GMM is normalized
        self.weights = np.round(self.weights, 5)  # prevent testing exact comparison problems

    def pdf_at(self, x: Union[np.ndarray, float], y: Union[np.ndarray, float]) -> Union[None, np.ndarray]:
        super(GMM2D, self).pdf_at(x, y)
        weighted_probabilities = np.array([self.weights[i] * g.pdf_at(x, y) for i, g in enumerate(self.gaussians)])
        return np.sum(weighted_probabilities, axis=0)

    def sample(self, num_samples: int) -> np.ndarray:
        mode_choices = np.random.choice(range(self.num_modes), size=num_samples, p=self.weights)
        return np.array([self.gaussians[mode].sample(1) for mode in mode_choices]).squeeze()

    def summary(self) -> Dict[str, Any]:
        summary = super(GMM2D, self).summary()
        summary.update({"gaussians": [g.summary() for g in self.gaussians], "weights": self.weights.tolist()})
        return summary

    @classmethod
    def from_summary(cls, json_text: Dict[str, Any]):
        super(GMM2D, cls).from_summary(json_text)
        gaussians = [Gaussian2D.from_summary(g) for g in json_text["gaussians"]]
        mus = np.reshape(np.array([g.mu for g in gaussians]), (-1, 2))
        sigmas = np.reshape(np.array([g.sigma for g in gaussians]), (-1, 2, 2))
        weights = np.array(json_text["weights"])
        return cls(mus, sigmas, weights)
