from pathlib import Path

from itest.test_setup import ExpressionTest


def find_expected(program_text):
    lines = program_text.splitlines()
    for line in lines:
        if line.startswith(";expected:"):
            return line.split(':')[1].strip()


class SampleProgramsTest(ExpressionTest):
    def setUp(self):
        super().setUp()
        top_directory = Path(__file__).parents[1]
        self.sample_programs_dir = Path(top_directory, "sample_programs")

    def test_all_samples(self):
        sample_programs = [p for p in self.sample_programs_dir.iterdir()]
        for program_file_path in sample_programs:
            print(f"running {program_file_path.name}")
            with program_file_path.open('r') as program_file:
                program_text = program_file.read()
                expected = find_expected(program_text)
                self.assertEqual(expected, self.evaluate(program_text))
