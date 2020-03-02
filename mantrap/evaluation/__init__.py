from typing import Any, Dict

from mantrap.utility.io import load_functions_from_module


# Aggregate metrics automatically as dictionary mapping the metric names to its function call,
# using the importlib and inspect module. In order to differentiate the metric functions from other, maybe imported,
# functions, they have to uniquely start with "metric_", e.g. a distance metric should be called "metric_distance".
def evaluate_metrics(**metric_kwargs) -> Dict[str, Any]:
    metrics = load_functions_from_module(module="mantrap.evaluation.metrics", prefix="metric_")
    assert len(metrics.keys()) > 0
    return {tag: function(**metric_kwargs) for tag, function in metrics.items()}
