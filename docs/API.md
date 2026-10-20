# API 参考

## 顶层

- `taskforge.Config` / `load_config(path)` / `default_config()`
- `taskforge.TaskforgeEngine(config)` — `.run(goal_id) -> WorkflowResult`

## planner

- `decompose(backend, goal_id, cfg) -> List[str]`
- `react_loop(backend, goal_id, cfg, observe) -> List[(action, obs)]`
- `ThinkingBudget(total, decay)` — `.allocate(n_steps)`

## tools

- `ToolRegistry()` — `.get(name)` / `.names()`
- `ToolOrchestrator(backend, cfg)` — `.execute(subgoal)`
- `ToolExecutor(max_calls)` — `.run(tool, args)`

## gui

- `screen_from_id(screen_id, n)` — `.elements`
- `ground_intent(backend, screen_id, intent_id) -> (element_id, action)`
- `GuiAgent(backend)` — `.act(screen_id, intent_id)`

## memory

- `WorkingMemory(cfg)` — `.mark_progress(subgoal)` / `.record_stall(subgoal)`
- `StallDetector(threshold)` — `.register(subgoal)`

## sparse

- `full_attention(q, keys)`
- `sparse_attention(q, keys, block_size, top_k, gold_blocks, skill, seq_key)`
- `BlockRouter(top_k)` — `.select(seq_key, n_blocks, gold_blocks, skill)`

## bench

- `run_all(cfg, backend) -> Dict[str, dict]` — planning / tools / gui / sparse / longhorizon
