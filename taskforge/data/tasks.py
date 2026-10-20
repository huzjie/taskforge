# -*- coding: utf-8 -*-
"""Task templates: natural-language goals mapped to deterministic subgoal plans."""
from __future__ import annotations

from typing import Dict, List

TASK_TEMPLATES: Dict[str, str] = {
    "sales_report": "整理本季度销售数据，生成报表并发送给团队",
    "customer_sync": "从 CRM 拉取客户信息，去重后同步到表格",
    "invoice_flow": "读取发票信息，校验金额并提交审批",
    "lead_enrich": "抓取线索网页，提取联系人并录入系统",
    "meeting_minutes": "读取会议录音转写，提炼行动项并派发任务",
}


def render_goal(template_key: str, idx: int = 0) -> str:
    """Return a natural-language goal string for a template key."""
    return TASK_TEMPLATES.get(template_key, TASK_TEMPLATES["sales_report"])
