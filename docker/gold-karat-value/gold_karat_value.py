"""Estimate gold melt and scrap value from karat, weight, and a 24K price per gram."""

from __future__ import annotations

import argparse
import json
import sys
from dataclasses import asdict, dataclass

GRAMS_PER_TROY_OUNCE = 31.1035
GRAMS_PER_PENNYWEIGHT = 1.55517384
GRAMS_PER_TROY_POUND = 373.242

UNITS = {
    "gram": 1.0,
    "pennyweight": GRAMS_PER_PENNYWEIGHT,
    "troy_ounce": GRAMS_PER_TROY_OUNCE,
    "troy_pound": GRAMS_PER_TROY_POUND,
    "kilogram": 1000.0,
}


class CalcError(ValueError):
    pass


@dataclass(frozen=True)
class MeltValue:
    total: float
    per_gram: float
    per_troy_ounce: float
    per_troy_pound: float


@dataclass(frozen=True)
class ScrapValue:
    market: float
    scrap: float


def _require_non_negative(value: float, message: str) -> float:
    if value != value or value in (float("inf"), float("-inf")) or value < 0:
        raise CalcError(message)
    return value


def to_grams(weight: float, unit: str) -> float:
    _require_non_negative(weight, "weight must be finite and non-negative")
    try:
        return weight * UNITS[unit]
    except KeyError as exc:
        raise CalcError("unit must be gram, pennyweight, troy_ounce, troy_pound, or kilogram") from exc


def purity_ratio(karat: float) -> float:
    if karat != karat or karat in (float("inf"), float("-inf")) or karat < 0 or karat > 24:
        raise CalcError("karat must be between 0 and 24")
    return karat / 24.0


def round_cents(amount: float) -> float:
    return round(amount * 100) / 100.0


def melt_value(weight: float, unit: str, karat: float, price_24k_per_gram: float) -> MeltValue:
    grams = to_grams(weight, unit)
    _require_non_negative(price_24k_per_gram, "price must be finite and non-negative")
    per_gram = round_cents(price_24k_per_gram * purity_ratio(karat))
    return MeltValue(
        total=round_cents(grams * per_gram),
        per_gram=per_gram,
        per_troy_ounce=round_cents(per_gram * GRAMS_PER_TROY_OUNCE),
        per_troy_pound=round_cents(per_gram * GRAMS_PER_TROY_POUND),
    )


def scrap_value(
    weight: float,
    unit: str,
    karat: float,
    price_24k_per_gram: float,
    discount: float,
) -> ScrapValue:
    if discount != discount or discount in (float("inf"), float("-inf")) or discount < 0 or discount > 1:
        raise CalcError("discount must be between 0 and 1")
    melt = melt_value(weight, unit, karat, price_24k_per_gram)
    return ScrapValue(market=melt.total, scrap=round_cents(melt.total * discount))


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Estimate gold melt and scrap value from karat, weight, and a 24K price per gram."
    )
    parser.add_argument("command", nargs="?", default="melt", choices=("melt", "scrap"))
    parser.add_argument("--weight", type=float, required=True)
    parser.add_argument("--unit", default="gram", choices=sorted(UNITS))
    parser.add_argument("--karat", type=float, required=True)
    parser.add_argument("--price", type=float, required=True, help="24K price per gram")
    parser.add_argument("--discount", type=float, default=0.85, help="scrap payout ratio, 0..1")
    parser.add_argument("--json", action="store_true")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    try:
        if args.command == "scrap":
            result = scrap_value(args.weight, args.unit, args.karat, args.price, args.discount)
        else:
            result = melt_value(args.weight, args.unit, args.karat, args.price)
    except CalcError as exc:
        print(exc, file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(asdict(result)))
        return 0

    if isinstance(result, ScrapValue):
        print(f"{int(args.discount * 100)}% scrap offer: ${result.scrap:.2f}")
    else:
        print(f"{args.karat:g}K melt: ${result.total:.2f} (${result.per_gram:.2f}/g)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
