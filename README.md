# gold-karat-value

Estimate gold melt value from karat, weight, and a 24K price per gram.

Jewelry and scrap workflows usually start from the same three inputs: how heavy the piece is, what karat stamp it carries, and what fine gold is trading at today. This library keeps that math in one place so a PHP script or backend can reuse the same rounding rules.

It does **not** call a price API. You pass in the 24K price you already have (spot feed, cached quote, or a number typed by the user).

## Install

```bash
composer require ilovejackylee/gold-karat-value
```

## Usage

```php
use GoldKaratValue\Calculator;

$melt = Calculator::meltValue(10.0, 'gram', 14.0, 65.0);
printf("14K melt: $%.2f ($%.2f/g)\n", $melt['total'], $melt['per_gram']);

$scrap = Calculator::scrapValue(10.0, 'gram', 14.0, 65.0, 0.85);
printf("85%% scrap offer: $%.2f\n", $scrap['scrap']);
```

Units: `gram`, `pennyweight`, `troy_ounce`, `troy_pound`, `kilogram`. Karat must be between `0` and `24` (including fractional stamps such as `21.6`).

## Formula

1. Convert the entered weight to grams.
2. Purity ratio = karat ÷ 24 (14K ≈ 0.5833).
3. Price per gram at that karat = 24K price per gram × ratio, rounded to cents.
4. Melt value = grams × that per-gram price, rounded to cents.
5. Scrap estimate = melt value × a payout ratio between 0 and 1 (for example 0.50 at a pawn shop, 0.85 for some online buyers).

The same cent-rounding is applied to per-gram, per-troy-ounce, and per-troy-pound quotes so table output stays consistent with a UI.

## When you need live prices

This library stops at the arithmetic. If you want the same karat and unit conversion with a regularly updated spot price in the browser, there is a [scrap gold calculator](https://mygoldcalc.com/scrap-gold-calculator) that applies these ratios without an account.

## License

MIT
