# GoldKaratValue

Estimate gold melt value from karat, weight, and a 24K price per gram.

Jewelry and scrap workflows usually start from the same three inputs: how heavy the piece is, what karat stamp it carries, and what fine gold is trading at today. This library keeps that math in one place so a .NET app or script can reuse the same rounding rules.

It does **not** call a price API. You pass in the 24K price you already have (spot feed, cached quote, or a number typed by the user).

## Install

```bash
dotnet add package GoldKaratValue
```

## Usage

```csharp
using GoldKaratValue;

var melt = Calculator.MeltValue(10, WeightUnit.Gram, 14, 65);
Console.WriteLine($"14K melt: ${melt.Total:0.00} (${melt.PerGram:0.00}/g)");

var scrap = Calculator.ScrapValue(10, WeightUnit.Gram, 14, 65, 0.85);
Console.WriteLine($"85% scrap offer: ${scrap.Scrap:0.00}");
```

`WeightUnit` covers grams, pennyweight, troy ounces, troy pounds, and kilograms. Karat must be between `0` and `24` (including fractional stamps such as `21.6`).

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
