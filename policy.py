"""Illustrative approval gate and cost model. Author: Feras Elghandour."""
from dataclasses import dataclass
from decimal import Decimal
import math

@dataclass(frozen=True)
class Claim:
    total_cents: int
    extraction_confidence: float
    receipt_type_verified: bool
    policy_compliant: bool

def route(claim, threshold_cents=50000, minimum_confidence=0.85):
    if type(claim.total_cents) is not int or claim.total_cents < 0:
        raise ValueError('Use nonnegative integer cents')
    if type(threshold_cents) is not int or threshold_cents < 0:
        raise ValueError('Invalid review threshold')
    if not math.isfinite(claim.extraction_confidence) or not 0 <= claim.extraction_confidence <= 1:
        raise ValueError('Invalid extraction confidence')
    if not 0 <= minimum_confidence <= 1:
        raise ValueError('Invalid confidence threshold')
    if claim.extraction_confidence < minimum_confidence or not claim.receipt_type_verified:
        return 'request_information'
    if not claim.policy_compliant:
        return 'reject'
    return 'human_review' if claim.total_cents > threshold_cents else 'eligible_for_approval'

def equal_split(total_cents, participants):
    if type(total_cents) is not int or total_cents < 0 or type(participants) is not int or participants < 1:
        raise ValueError('Invalid allocation')
    base, remainder = divmod(total_cents, participants)
    return tuple(base + (i < remainder) for i in range(participants))

def monthly_cost(reports, model_cost_per_report, review_fraction, review_minutes, hourly_rate, fixed_cost):
    values=[Decimal(str(v)) for v in [reports,model_cost_per_report,review_fraction,review_minutes,hourly_rate,fixed_cost]]
    if any(not v.is_finite() or v < 0 for v in values) or values[2] > 1:
        raise ValueError('Invalid cost assumptions')
    n, model, share, minutes, rate, fixed = values
    return fixed + n * (model + share * minutes * rate / 60)
