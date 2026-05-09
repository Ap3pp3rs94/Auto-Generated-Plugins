from __future__ import annotations

import unittest
from pathlib import Path
import sys


FRANCIS_ROOT = Path(__file__).resolve().parents[2]
if str(FRANCIS_ROOT) not in sys.path:
    sys.path.insert(0, str(FRANCIS_ROOT))

from factory.factory_runner import RunnerConfig, build_config_from_args


class RunnerConfigTests(unittest.TestCase):
    def test_once_mode_builds_one_plugin(self) -> None:
        config, log_level, print_config = build_config_from_args(["--once", "--print-config"])

        self.assertEqual(config.max_plugins, 1)
        self.assertFalse(config.loop_forever)
        self.assertEqual(log_level, "INFO")
        self.assertTrue(print_config)

    def test_max_plugins_disables_loop_mode(self) -> None:
        config, _, _ = build_config_from_args(["--max-plugins", "3"])

        self.assertEqual(config.max_plugins, 3)
        self.assertFalse(config.loop_forever)

    def test_invalid_temperature_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RunnerConfig(llm_temperature=3.0).validate()

    def test_invalid_timeout_is_rejected(self) -> None:
        with self.assertRaises(ValueError):
            RunnerConfig(llm_timeout_seconds=0).validate()


if __name__ == "__main__":
    unittest.main()
