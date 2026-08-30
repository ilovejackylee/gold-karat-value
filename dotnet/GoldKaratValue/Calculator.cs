namespace GoldKaratValue;

/// <summary>Weight unit accepted by the calculator.</summary>
public enum WeightUnit
{
    Gram,
    Pennyweight,
    TroyOunce,
    TroyPound,
    Kilogram
}

/// <summary>Why a calculation was rejected.</summary>
public enum CalcError
{
    NegativeWeight,
    InvalidKarat,
    NegativePrice,
    InvalidDiscount
}

public sealed class CalcException : Exception
{
    public CalcError Error { get; }

    public CalcException(CalcError error, string message) : base(message)
    {
        Error = error;
    }
}

/// <summary>Breakdown of melt value after applying karat purity.</summary>
public readonly record struct MeltValue(
    decimal Total,
    decimal PerGram,
    decimal PerTroyOunce,
    decimal PerTroyPound);

/// <summary>Melt value plus a buyer-style scrap estimate.</summary>
public readonly record struct ScrapValue(decimal Market, decimal Scrap);

/// <summary>
/// Estimate gold melt and scrap value from karat, weight, and a 24K price per gram.
/// Does not fetch live market data.
/// </summary>
public static class Calculator
{
    public const double GramsPerTroyOunce = 31.1035;
    public const double GramsPerPennyweight = 1.55517384;
    public const double GramsPerTroyPound = 373.242;

    public static double GramsPerUnit(WeightUnit unit) => unit switch
    {
        WeightUnit.Gram => 1.0,
        WeightUnit.Pennyweight => GramsPerPennyweight,
        WeightUnit.TroyOunce => GramsPerTroyOunce,
        WeightUnit.TroyPound => GramsPerTroyPound,
        WeightUnit.Kilogram => 1000.0,
        _ => throw new ArgumentOutOfRangeException(nameof(unit))
    };

    public static double ToGrams(double weight, WeightUnit unit)
    {
        RequireNonNegative(weight, CalcError.NegativeWeight, "weight must be finite and non-negative");
        return weight * GramsPerUnit(unit);
    }

    public static double PurityRatio(double karat)
    {
        if (double.IsNaN(karat) || double.IsInfinity(karat) || karat < 0 || karat > 24)
        {
            throw new CalcException(CalcError.InvalidKarat, "karat must be between 0 and 24");
        }

        return karat / 24.0;
    }

    public static decimal RoundCents(double amount) =>
        Math.Round((decimal)amount, 2, MidpointRounding.AwayFromZero);

    public static MeltValue MeltValue(double weight, WeightUnit unit, double karat, double price24kPerGram)
    {
        var grams = ToGrams(weight, unit);
        RequireNonNegative(price24kPerGram, CalcError.NegativePrice, "price must be finite and non-negative");
        var perGram = RoundCents(price24kPerGram * PurityRatio(karat));

        return new MeltValue(
            Total: RoundCents(grams * (double)perGram),
            PerGram: perGram,
            PerTroyOunce: RoundCents((double)perGram * GramsPerTroyOunce),
            PerTroyPound: RoundCents((double)perGram * GramsPerTroyPound));
    }

    public static ScrapValue ScrapValue(
        double weight,
        WeightUnit unit,
        double karat,
        double price24kPerGram,
        double discount)
    {
        if (double.IsNaN(discount) || double.IsInfinity(discount) || discount < 0 || discount > 1)
        {
            throw new CalcException(CalcError.InvalidDiscount, "discount must be between 0 and 1");
        }

        var melt = MeltValue(weight, unit, karat, price24kPerGram);
        return new ScrapValue(melt.Total, RoundCents((double)melt.Total * discount));
    }

    private static void RequireNonNegative(double value, CalcError error, string message)
    {
        if (double.IsNaN(value) || double.IsInfinity(value) || value < 0)
        {
            throw new CalcException(error, message);
        }
    }
}
