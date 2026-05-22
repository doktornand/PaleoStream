"""
Rule Engine - Moteur de regles hierarchiques
"""

import json
from typing import Dict, List, Any, Optional
from pathlib import Path

class HierarchicalRuleEngine:
    def __init__(self, config_path: str = "config/hierarchical_rules.json"):
        self.rules = self._load_rules(config_path)
        self.cascade_order = self.rules.get("rule_engine", {}).get("cascade_order", [])
        self.priority_levels = self.rules.get("rule_engine", {}).get("priority_levels", [])
        self.applied_rules: List[Dict] = []
        self.conflicts: List[Dict] = []
        self.fallbacks: List[str] = []

    def _load_rules(self, path: str) -> Dict:
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            return {"rule_engine": {}, "fallback_rules": {}}

    def evaluate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        self.applied_rules = []
        self.conflicts = []
        self.fallbacks = []

        result = {
            "transformations": [],
            "warnings": [],
            "manual_review": [],
            "metadata": {
                "rules_evaluated": 0,
                "rules_applied": 0,
                "conflicts_resolved": 0,
                "fallback_triggers": 0
            }
        }

        for category_name in self.cascade_order:
            category = self.rules.get(category_name)
            if not category:
                continue

            category_result = self._evaluate_category(category, category_name, context)

            result["transformations"].extend(category_result["transformations"])
            result["warnings"].extend(category_result["warnings"])
            result["manual_review"].extend(category_result["manual_review"])
            result["metadata"]["rules_evaluated"] += category_result["evaluated"]
            result["metadata"]["rules_applied"] += category_result["applied"]

        if not result["transformations"]:
            fallback = self._apply_fallback(context)
            if fallback:
                result["manual_review"].append(fallback)
                result["metadata"]["fallback_triggers"] += 1

        result["metadata"]["conflicts_resolved"] = len(self.conflicts)
        return result

    def _evaluate_category(self, category: Dict, category_name: str, context: Dict) -> Dict:
        result = {
            "transformations": [],
            "warnings": [],
            "manual_review": [],
            "evaluated": 0,
            "applied": 0
        }

        priority = category.get("_priority", "LOW")
        rules = category.get("rules", [])

        for rule in rules:
            result["evaluated"] += 1

            match_result = self._match_rule(rule, context)
            if match_result["matched"]:
                result["applied"] += 1

                conflicts = self._detect_conflicts(rule, match_result.get("bindings", {}))
                if conflicts:
                    resolution = self._resolve_conflicts(rule, conflicts, priority)
                    self.conflicts.extend(resolution.get("conflicts", []))
                    if not resolution.get("keep_rule", True):
                        continue

                self.applied_rules.append({
                    "category": category_name,
                    "priority": priority,
                    "rule": rule.get("id"),
                    "bindings": match_result.get("bindings", {})
                })

                transforms = self._extract_transformations(rule, match_result.get("bindings", {}))
                result["transformations"].extend(transforms)

                if "warnings" in rule:
                    result["warnings"].extend([
                        {"rule": rule["id"], "message": w}
                        for w in rule["warnings"]
                    ])

                if self._requires_manual_review(rule, context):
                    result["manual_review"].append({
                        "rule": rule["id"],
                        "reason": self._get_manual_review_reason(rule),
                        "confidence": match_result.get("confidence", 1.0)
                    })

        return result

    def _match_rule(self, rule: Dict, context: Dict) -> Dict:
        condition = rule.get("condition", {})
        bindings = {}
        confidence = 1.0

        for key, expected in condition.items():
            actual = context.get(key)

            if actual is None:
                return {"matched": False}

            if isinstance(expected, str) and "|" in expected:
                alternatives = [s.strip() for s in expected.split("|")]
                if str(actual) not in alternatives:
                    return {"matched": False}
                bindings[key] = actual
            elif isinstance(expected, list):
                if actual not in expected:
                    return {"matched": False}
                bindings[key] = actual
            elif isinstance(expected, dict):
                complex_match = self._match_complex(expected, actual)
                if not complex_match["matched"]:
                    return {"matched": False}
                bindings[key] = actual
                confidence *= complex_match.get("confidence", 1.0)
            else:
                if actual != expected:
                    return {"matched": False}
                bindings[key] = actual

        return {"matched": True, "bindings": bindings, "confidence": confidence}

    def _match_complex(self, expected: Dict, actual: Any) -> Dict:
        if "gt" in expected:
            return {"matched": actual > expected["gt"], "confidence": 0.9}
        if "lt" in expected:
            return {"matched": actual < expected["lt"], "confidence": 0.9}
        if "regex" in expected:
            import re
            matched = bool(re.search(expected["regex"], str(actual)))
            return {"matched": matched, "confidence": 1.0 if matched else 0.0}
        return {"matched": False, "confidence": 0}

    def _detect_conflicts(self, new_rule: Dict, new_bindings: Dict) -> List[Dict]:
        conflicts = []
        for applied in self.applied_rules:
            if self._has_same_target(new_rule, applied["rule"]):
                conflicts.append({
                    "existing": applied,
                    "new": new_rule.get("id"),
                    "target": self._get_transformation_target(new_rule)
                })
        return conflicts

    def _resolve_conflicts(self, new_rule: Dict, conflicts: List[Dict], new_priority: str) -> Dict:
        new_priority_idx = self.priority_levels.index(new_priority) if new_priority in self.priority_levels else 999
        keep_rule = True
        resolved = []

        for conflict in conflicts:
            existing_priority_idx = self.priority_levels.index(conflict["existing"]["priority"]) if conflict["existing"]["priority"] in self.priority_levels else 999

            if new_priority_idx < existing_priority_idx:
                resolved.append({
                    "type": "OVERRIDE",
                    "winner": new_rule.get("id"),
                    "loser": conflict["existing"]["rule"],
                    "reason": f"Priorite {new_priority} > {conflict['existing']['priority']}"
                })
            elif new_priority_idx > existing_priority_idx:
                keep_rule = False
                resolved.append({
                    "type": "REJECTED",
                    "winner": conflict["existing"]["rule"],
                    "loser": new_rule.get("id"),
                    "reason": f"Priorite {conflict['existing']['priority']} > {new_priority}"
                })
            else:
                resolved.append({
                    "type": "UNRESOLVED",
                    "rules": [conflict["existing"]["rule"], new_rule.get("id")],
                    "reason": "Meme priorite - necessite decision manuelle"
                })
                keep_rule = False

        return {"conflicts": resolved, "keep_rule": keep_rule}

    def _extract_transformations(self, rule: Dict, bindings: Dict) -> List[Dict]:
        transforms = []
        transformations = rule.get("transformations", {})

        for key, value in transformations.items():
            transforms.append({
                "type": key,
                "rule": rule.get("id"),
                "data": self._substitute_bindings(value, bindings),
                "original": rule.get("condition", {})
            })

        return transforms

    def _substitute_bindings(self, template: Any, bindings: Dict) -> Any:
        if isinstance(template, str):
            result = template
            for key, value in bindings.items():
                result = result.replace(f"{{{key}}}", str(value))
            return result
        elif isinstance(template, list):
            return [self._substitute_bindings(item, bindings) for item in template]
        elif isinstance(template, dict):
            return {k: self._substitute_bindings(v, bindings) for k, v in template.items()}
        return template

    def _requires_manual_review(self, rule: Dict, context: Dict) -> bool:
        high_risk = [
            "pattern_far_calls",
            "pattern_self_modifying",
            "pattern_interrupt_hooks",
            "pattern_dollar_strings"
        ]
        return rule.get("id") in high_risk

    def _get_manual_review_reason(self, rule: Dict) -> str:
        reasons = {
            "pattern_far_calls": "Graphe d'appel complexe - necessite analyse manuelle",
            "pattern_self_modifying": "Code auto-modifiant - risque de securite",
            "pattern_interrupt_hooks": "Hooks d'interruption - comportement critique",
            "pattern_dollar_strings": "Chaines DOS $ - verifier la longueur calculee"
        }
        return reasons.get(rule.get("id"), "Pattern complexe detecte")

    def _apply_fallback(self, context: Dict) -> Optional[Dict]:
        fallback = self.rules.get("fallback_rules", {})
        rules = fallback.get("rules", [])

        for rule in rules:
            if rule.get("condition", {}).get("match") == "no_rule_applied" and not self.applied_rules:
                self.fallbacks.append(rule.get("id", ""))
                return {
                    "rule": rule.get("id"),
                    "marker": rule.get("action", {}).get("marker"),
                    "message": rule.get("action", {}).get("output"),
                    "type": "FALLBACK"
                }
        return None

    def _has_same_target(self, rule1: Dict, rule2_id: str) -> bool:
        return rule1.get("id", "").split("_")[0] == rule2_id.split("_")[0]

    def _get_transformation_target(self, rule: Dict) -> str:
        transforms = rule.get("transformations", {})
        return list(transforms.keys())[0] if transforms else "unknown"

    def generate_report(self) -> Dict:
        return {
            "applied_rules": self.applied_rules,
            "conflicts": self.conflicts,
            "fallbacks": self.fallbacks,
            "summary": {
                "total_rules": len(self.applied_rules),
                "critical_rules": len([r for r in self.applied_rules if r["priority"] == "CRITICAL"]),
                "high_rules": len([r for r in self.applied_rules if r["priority"] == "HIGH"]),
                "manual_reviews": len([r for r in self.applied_rules if r["rule"] in [
                    "pattern_far_calls", "pattern_self_modifying", "pattern_interrupt_hooks"
                ]])
            }
        }
