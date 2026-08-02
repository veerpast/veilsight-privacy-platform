import unittest

from app.benchmark import intersection_over_union, precision_recall
from app.models import FaceBox


class BenchmarkTests(unittest.TestCase):
    def test_iou_identical_boxes(self) -> None:
        box = FaceBox(10, 10, 20, 20)
        self.assertEqual(intersection_over_union(box, box), 1.0)

    def test_precision_recall_one_match_one_false_positive(self) -> None:
        truth = [FaceBox(10, 10, 20, 20)]
        predictions = [FaceBox(10, 10, 20, 20, 0.9), FaceBox(60, 60, 10, 10, 0.7)]
        precision, recall = precision_recall(predictions, truth)
        self.assertEqual(precision, 0.5)
        self.assertEqual(recall, 1.0)


if __name__ == "__main__":
    unittest.main()
