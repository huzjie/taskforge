# -*- coding: utf-8 -*-
"""Action grounding: natural-language intent -> (element, action) pair.

The mock backend grounds an intent by picking the target element with probability
``p = 0.5 + 0.5*boost`` (boost = (skill - 0.5) * 2) and a legal action otherwise.
"""
from __future__ import annotations

from typing import Dict, Tuple

from ..oracle import ACTIONS, ground_correct, screen_elements, target_element


def ground_intent(backend, screen_id: str, intent_id: str) -> Tuple[str, str]:
    """Returns (element_id, action)."""
    elements = screen_elements(screen_id)
    return backend.ground(screen_id, intent_id, elements)


def grounding_ok(backend, screen_id: str, intent_id: str) -> bool:
    elements = screen_elements(screen_id)
    element_id, action = backend.ground(screen_id, intent_id, elements)
    return ground_correct(screen_id, intent_id, element_id, action)
