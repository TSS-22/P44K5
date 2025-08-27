import unittest

from logic import reset_key_degree, compute_pad_intervals, note_off

class test_resetKeyDegree(unittest.TestCase):
    def test_return0(self):
        self.assertEqual(reset_key_degree(), 0)

class test_padInterval(unittest.TestCase):

    t_tone_progression = [
            2,
            2,
            1,
            2,
            2,
            2,
            1,
        ]

    def test_intervalCompute(self):
        for val in range(8):
            self.assertEqual(compute_pad_intervals(val),([-x for x in self.t_tone_progression[:val]] + [0] + self.t_tone_progression[val:]))

class test_noteOff(unittest.TestCase):
    
    def test_run(self):
        self.assertEqual(note_off())

        


if __name__ == '__main__':
    unittest.main(verbosity=2)