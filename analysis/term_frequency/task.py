"""
"<Paper Title>"
<Paper URL>

<Paper Abstract>

NOTE: Notes
"""
from lm_eval.base import Task, rf
from lm_eval.metrics import mean


_CITATION = """

"""

class NumericalReasoningBaseTask(Task):
    VERSION = 1.0
    DATASET_PATH = "numerical_reasoning_arithmetic.py"
    DATASET_NAME = None

    def __init__(self, data_dir=None, cache_dir=None, download_mode=None, DATASET_NAME=None):

        self.DATASET_NAME = DATASET_NAME
        self.download(data_dir, cache_dir, download_mode)
        self._training_docs = None
        self._fewshot_docs = None

    def has_training_docs(self):
        return False

    def has_validation_docs(self):
        return False

    def has_test_docs(self):
        return True

    def training_docs(self):
        return NotImplementedError

    def validation_docs(self):
        raise NotImplementedError

    def test_docs(self):
        return self.dataset["test"]

    def doc_to_text(self, doc):
        raise NotImplementedError

    def doc_to_target(self, doc):
        raise NotImplementedError

    def construct_requests(self, doc, ctx):
        """Uses RequestFactory to construct Requests and returns an iterable of
        Requests which will be sent to the LM.

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param ctx: str
            The context string, generated by fewshot_context. This includes the natural
            language description, as well as the few shot examples, and the question
            part of the document for `doc`.
        """
        # NOTE: The paper implements "verifiers" that assign a score to multiple
        # solutions and output the highest ranked solution.
        completion = rf.greedy_until(ctx, "\n")
        return completion

    def _get_answer(self, doc):
        raise NotImplementedError

    def process_results(self, doc, results):
        """Take a single document and the LM results and evaluates, returning a
        dict where keys are the names of submetrics and values are the values of
        the metric for that one document

        :param doc:
            The document as returned from training_docs, validation_docs, or test_docs.
        :param results:
            The results of the requests created in construct_requests.
        """
        completion = results[0]
        gold = self.doc_to_target(doc)

        acc = 1.0 if completion == gold else 0.0

        return {"acc": acc}

    def aggregation(self):
        """
        :returns: {str: [float] -> float}
            A dictionary where keys are the names of submetrics and values are
            functions that aggregate a list of metrics
        """
        return {"acc": mean}

    def higher_is_better(self):
        """
        :returns: {str: bool}
            A dictionary where keys are the names of submetrics and values are
            whether a higher value of the submetric is better
        """
        return {"acc": True}


class ArithmeticMultiplication(NumericalReasoningBaseTask):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_arithmetic_multiplication",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x1} times {x2}? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_mul}".format(**doc)


class ArithmeticAddition(NumericalReasoningBaseTask):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_arithmetic_addition",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x1} plus {x2}? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_add}".format(**doc)


class OperationInferenceMult(NumericalReasoningBaseTask):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_op_infer_multiplication",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x1} # {x2}? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_mul}".format(**doc)


class OperationInferenceAdd(NumericalReasoningBaseTask):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_op_infer_addition",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x1} # {x2}? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_add}".format(**doc)


class TimeUnitInferenceMinSec(NumericalReasoningBaseTask):

    DATASET_PATH = "numerical_reasoning_time_unit_conversion.py"

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_min_sec",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} minutes in seconds? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_min_sec}".format(**doc)


class TimeUnitInferenceHourMin(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_hour_min",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} hours in minutes? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_hour_min}".format(**doc)


class TimeUnitInferenceDayHour(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_day_hour",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} days in hours? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_day_hour}".format(**doc)


class TimeUnitInferenceWeekDay(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_week_day",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} weeks in days? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_week_day}".format(**doc)


class TimeUnitInferenceMonthWeek(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_month_week",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} months in weeks? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_month_week}".format(**doc)


class TimeUnitInferenceYearMonth(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_year_month",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} years in months? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_year_month}".format(**doc)


class TimeUnitInferenceDecadeYear(TimeUnitInferenceMinSec):

    def __init__(self, DATASET_NAME):
        super().__init__(DATASET_NAME=DATASET_NAME)
        self.EVAL_HARNESS_NAME = "{}_{}".format(
            "num_reasoning_convert_decade_year",
            self.DATASET_NAME
        )

    def doc_to_text(self, doc):
        return "Q: What is {x} decades in years? A:".format(**doc)

    def doc_to_target(self, doc):
        return "{y_decade_year}".format(**doc)
