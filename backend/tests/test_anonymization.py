import unittest

import numpy as np

from app.anonymization import anonymize_faces
from app.models import FaceBox


class AnonymizationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.image = np.full((80, 100, 3), 180, dtype=np.uint8)
        self.image[20:60, 30:70] = np.arange(40, dtype=np.uint8)[:, None, None]
        self.face = FaceBox(30, 20, 40, 40)

    def test_original_is_not_mutated(self) -> None:
        original = self.image.copy()
        anonymize_faces(self.image, [self.face], "solid", 0.8)
        np.testing.assert_array_equal(self.image, original)

    def test_solid_changes_only_face_region(self) -> None:
        result = anonymize_faces(self.image, [self.face], "solid", 0.8)
        np.testing.assert_array_equal(result[:20], self.image[:20])
        self.assertTrue(np.all(result[20:60, 30:70] == (15, 35, 59)))

    def test_boxes_are_clipped(self) -> None:
        result = anonymize_faces(self.image, [FaceBox(-10, -10, 30, 30)], "pixelate", 0.5)
        self.assertEqual(result.shape, self.image.shape)


if __name__ == "__main__":
    unittest.main()
