# gold-karat-value

Estimate gold melt value from karat, weight, and a 24K price per gram.

Jewelry and scrap workflows usually start from the same three inputs: how heavy the piece is, what karat stamp it carries, and what fine gold is trading at today. This image keeps that math in one CLI so a container, CI job, or script can reuse the same rounding rules.

It does **not** call a price API. You pass in the 24K price you already have (spot feed, cached quote, or a number typed by the user).

## Pull

```bash
docker pull hiltonlee981/gold-karat-value
```

## Usage

```bash
docker run --rm hiltonlee981/gold-karat-value \
  --weight 10 --unit gram --karat 14 --price 65

docker run --rm hiltonlee981/gold-karat-value scrap \
  --weight 10 --unit gram --karat 14 --price 65 --discount 0.85
```

`--unit` accepts `gram`, `pennyweight`, `troy_ounce`, `troy_pound`, and `kilogram`. Karat must be between `0` and `24` (including fractional stamps such as `21.6`). Add `--json` for machine-readable output.

## Formula

1. Convert the entered weight to grams.
2. Purity ratio = karat ÷ 24 (14K ≈ 0.5833).
3. Price per gram at that karat = 24K price per gram × ratio, rounded to cents.
4. Melt value = grams × that per-gram price, rounded to cents.
5. Scrap estimate = melt value × a payout ratio between 0 and 1 (for example 0.50 at a pawn shop, 0.85 for some online buyers).

The same cent-rounding is applied to per-gram, per-troy-ounce, and per-troy-pound quotes so table output stays consistent with a UI.

## When you need live prices

This image stops at the arithmetic. If you want the same karat and unit conversion with a regularly updated spot price in the browser, there is a [scrap gold calculator](https://mygoldcalc.com/scrap-gold-calculator) that applies these ratios without an account.

## License

MIT
