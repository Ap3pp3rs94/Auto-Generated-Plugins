from __future__ import annotations

import unittest
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
FRANCIS_ROOT = Path(__file__).resolve().parents[2]
for path in (REPO_ROOT, FRANCIS_ROOT):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

try:
    from factory.factory_runner import RunnerConfig, build_config_from_args
except ModuleNotFoundError:
    from factory_runner import RunnerConfig, build_config_from_args


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

    def test_github_publish_defaults_to_enabled(self) -> None:
        config, _, _ = build_config_from_args(["--once"])

        self.assertTrue(config.github_publish_enabled)
        self.assertEqual(config.github_remote, "origin")
        self.assertEqual(config.github_branch, "main")

    def test_github_publish_can_be_disabled(self) -> None:
        config, _, _ = build_config_from_args(["--once", "--no-github-publish"])

        self.assertFalse(config.github_publish_enabled)

    def test_invalid_github_remote_is_rejected_when_enabled(self) -> None:
        with self.assertRaises(ValueError):
            RunnerConfig(github_remote="").validate()


if __name__ == "__main__":
    unittest.main()
