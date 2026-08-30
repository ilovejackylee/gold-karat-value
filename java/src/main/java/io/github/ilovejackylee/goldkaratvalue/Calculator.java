package io.github.ilovejackylee.goldkaratvalue;

/**
 * Estimate gold melt and scrap value from karat, weight, and a 24K price per gram.
 * Does not fetch live market data.
 */
public final class Calculator {
    public static final double GRAMS_PER_TROY_OUNCE = 31.1035;
    public static final double GRAMS_PER_PENNYWEIGHT = 1.55517384;
    public static final double GRAMS_PER_TROY_POUND = 373.242;

    private Calculator() {
    }

    public static double gramsPerUnit(WeightUnit unit) {
        switch (unit) {
            case GRAM:
                return 1.0;
            case PENNYWEIGHT:
                return GRAMS_PER_PENNYWEIGHT;
            case TROY_OUNCE:
                return GRAMS_PER_TROY_OUNCE;
            case TROY_POUND:
                return GRAMS_PER_TROY_POUND;
            case KILOGRAM:
                return 1000.0;
            default:
                throw new IllegalArgumentException("unknown unit: " + unit);
        }
    }

    public static double toGrams(double weight, WeightUnit unit) {
        requireNonNegative(weight, CalcError.NEGATIVE_WEIGHT);
        return weight * gramsPerUnit(unit);
    }

    public static double purityRatio(double karat) {
        if (!Double.isFinite(karat) || karat < 0 || karat > 24) {
            throw new CalcException(CalcError.INVALID_KARAT, "karat must be between 0 and 24");
        }
        return karat / 24.0;
    }

    public static double roundCents(double amount) {
        return Math.round(amount * 100.0) / 100.0;
    }

    public static MeltValue meltValue(double weight, WeightUnit unit, double karat, double price24kPerGram) {
        double grams = toGrams(weight, unit);
        requireNonNegative(price24kPerGram, CalcError.NEGATIVE_PRICE);
        double perGram = roundCents(price24kPerGram * purityRatio(karat));
        return new MeltValue(
                roundCents(grams * perGram),
                perGram,
                roundCents(perGram * GRAMS_PER_TROY_OUNCE),
                roundCents(perGram * GRAMS_PER_TROY_POUND));
    }

    public static ScrapValue scrapValue(
            double weight,
            WeightUnit unit,
            double karat,
            double price24kPerGram,
            double discount) {
        if (!Double.isFinite(discount) || discount < 0 || discount > 1) {
            throw new CalcException(CalcError.INVALID_DISCOUNT, "discount must be between 0 and 1");
        }
        MeltValue melt = meltValue(weight, unit, karat, price24kPerGram);
        return new ScrapValue(melt.total, roundCents(melt.total * discount));
    }

    private static void requireNonNegative(double value, CalcError error) {
        if (!Double.isFinite(value) || value < 0) {
            throw new CalcException(error, "value must be finite and non-negative");
        }
    }
}
