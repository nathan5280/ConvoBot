import unittest, os
from src.convobot.util.FilenameManager import FilenameManager

theta = 45.2
radius = 15.6
alpha = 90

theta_l = '045.2'
radius_l = '15.6'
alpha_l = '090'
filename = '045.2_15.6_090.png'
path = 'data'

class FilenameManagerTest(unittest.TestCase):
    def test_label_to_filename(self):
        fm = FilenameManager()
        fn = fm.label_to_filename(theta, radius, alpha)
        self.assertEqual(filename, fn)

    def test_label_to_filename_alt(self):
        filename = '045.2-15.6-090.xyz'
        fm = FilenameManager(separator='-', extension='xyz')
        fn = fm.label_to_filename(theta, radius, alpha)
        self.assertEqual(filename, fn)

    def test_label_to_path(self):
        fm = FilenameManager()
        fn = fm.label_to_path(path, theta, radius, alpha)
        self.assertEqual(os.path.join(path, filename), fn)

    def test_label_to_radius_path(self):
        fm = FilenameManager()
        fn = fm.label_to_radius_path(path, theta, radius, alpha)
        self.assertEqual(os.path.join(path, '{:04.1f}'.format(radius), filename), fn)

    def test_filename_to_labels(self):
        fm = FilenameManager()
        t, r, a = fm.filename_to_labels(filename)
        self.assertEqual(theta_l, t)
        self.assertEqual(radius_l, r)
        self.assertEqual(alpha_l, a)

    def test_filename_to_labels_alt(self):
        filename = '045.2-15.6-090.xyz'
        fm = FilenameManager(separator='-', extension='xyz')
        t, r, a = fm.filename_to_labels(filename)
        self.assertEqual(theta_l, t)
        self.assertEqual(radius_l, r)
        self.assertEqual(alpha_l, a)

    def test_filename_to_theta(self):
        fm = FilenameManager()
        t = fm.filename_to_theta(filename)
        self.assertEqual(theta_l, t)

    def test_filename_to_radius(self):
        fm = FilenameManager()
        r = fm.filename_to_radius(filename)
        self.assertEqual(radius_l, r)

    def test_filename_to_alpha(self):
        fm = FilenameManager()
        a = fm.filename_to_alpha(filename)
        self.assertEqual(alpha_l, a)

if __name__ == '__main__':
    unittest.main()
