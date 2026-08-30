from __future__ import annotations

import unittest

from gaussian_robotics_atlas.query import recommend, search

from tests.helpers import resource


def catalog():
    return (
        resource(),
        resource(
            id="grasp-splats",
            name="Grasp Splats",
            category="manipulation-interaction",
            summary=(
                "Predicts collision-aware grasps from a compact Gaussian representation of the "
                "workspace."
            ),
            inputs=("rgb",),
            frameworks=("ros2", "pytorch"),
            capabilities=("grasping",),
            tags=("mobile-manipulation",),
            year=2026,
            code_status="partial",
            code_url="https://github.com/example/grasp-splats",
            doi="10.1000/grasp-splats",
            arxiv="2601.12345",
            featured=False,
            sources=("https://github.com/example/grasp-splats",),
        ),
        resource(
            id="semantic-paper",
            name="Semantic Paper",
            category="semantic-perception",
            summary=(
                "Adds open vocabulary features to Gaussian scenes for reusable semantic "
                "perception."
            ),
            inputs=("rgb",),
            frameworks=("pytorch",),
            capabilities=("open-vocabulary",),
            tags=(),
            code_status="paper-only",
            code_url=None,
            doi="10.1000/semantic-paper",
            arxiv="2501.54321",
            featured=False,
            sources=("https://example.org/semantic-paper",),
        ),
    )


class SearchTests(unittest.TestCase):
    def test_composes_text_and_faceted_filters(self) -> None:
        found = search(
            catalog(),
            "collision grasps",
            category="manipulation-interaction",
            input_type="rgb",
            framework="ros2",
            code_status="partial",
        )
        self.assertEqual([item.id for item in found], ["grasp-splats"])

    def test_exact_name_beats_other_text_matches(self) -> None:
        exact = resource(
            name="Online",
            id="online",
            summary="Maintains a map for robot localization during deployment.",
        )
        results = search((*catalog(), exact), "Online")
        self.assertEqual(results[0].id, "online")


class RecommendationTests(unittest.TestCase):
    def test_recommendations_are_explainable_and_task_aware(self) -> None:
        results = recommend(
            catalog(),
            "manipulation",
            sensor="rgb",
            framework="ros2",
        )
        self.assertEqual(results[0].resource.id, "grasp-splats")
        self.assertGreater(results[0].score, 0)
        self.assertIn("task category: manipulation-interaction", results[0].reasons)
        self.assertIn("sensor input: rgb", results[0].reasons)
        self.assertIn("framework: ros2", results[0].reasons)

    def test_code_requirement_and_limit_are_honored(self) -> None:
        without_papers = recommend(catalog(), "semantics")
        self.assertNotIn("semantic-paper", [item.resource.id for item in without_papers])
        with_papers = recommend(catalog(), "semantics", require_code=False, limit=1)
        self.assertEqual(len(with_papers), 1)
        self.assertEqual(with_papers[0].resource.id, "semantic-paper")
        self.assertEqual(recommend(catalog(), "slam", limit=0), ())


if __name__ == "__main__":
    unittest.main()
