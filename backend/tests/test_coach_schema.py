from backend.app.schemas.coach import AdaptiveDebriefContent


def test_adaptive_debrief_content_accepts_valid_structure() -> None:
    debrief = AdaptiveDebriefContent(
        performance_summary="The learner recognized deterioration.",
        strengths=["Escalated care early."],
        improvement_priorities=["Activate transfusion sooner."],
        clinical_reasoning_explanation=(
            "Progressive tachycardia and hypotension suggested ongoing blood loss."
        ),
        replay_objective="Recognize and treat hemorrhagic shock earlier.",
        replay_success_criteria=[
            "Call for help within 60 seconds.",
            "Activate transfusion within 120 seconds.",
        ],
    )

    assert debrief.strengths == ["Escalated care early."]
    assert len(debrief.replay_success_criteria) == 2
