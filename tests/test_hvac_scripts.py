import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

import ezdxf


ROOT = Path(__file__).resolve().parents[1]


class HvacScriptsSmokeTest(unittest.TestCase):
    def test_scripts_generate_expected_layers(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_path = Path(tmp)
            source = tmp_path / "input.dxf"
            pipes = tmp_path / "pipes.dxf"
            combined = tmp_path / "pipes_ducts.dxf"

            ezdxf.new("R2018").saveas(source)

            subprocess.run(
                [sys.executable, "hvac_pipes.py", str(source), str(pipes)],
                cwd=ROOT,
                check=True,
            )
            subprocess.run(
                [sys.executable, "hvac_ducts.py", str(pipes), str(combined)],
                cwd=ROOT,
                check=True,
            )

            self.assertTrue(pipes.exists())
            self.assertTrue(combined.exists())

            pipe_doc = ezdxf.readfile(pipes)
            pipe_layers = {layer.dxf.name for layer in pipe_doc.layers}
            self.assertTrue({"P-CHWS", "P-CHWR", "P-CHW-TXT"}.issubset(pipe_layers))
            self.assertGreater(len(pipe_doc.modelspace()), 0)

            combined_doc = ezdxf.readfile(combined)
            combined_layers = {layer.dxf.name for layer in combined_doc.layers}
            self.assertTrue(
                {
                    "P-CHWS",
                    "P-CHWR",
                    "M-DUCT-SA",
                    "M-DIFUSER",
                    "M-AHU",
                }.issubset(combined_layers)
            )
            self.assertGreater(len(combined_doc.modelspace()), len(pipe_doc.modelspace()))


if __name__ == "__main__":
    unittest.main()
