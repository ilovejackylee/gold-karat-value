package io.github.ilovejackylee.goldkaratvalue;

/** Breakdown of melt value after applying karat purity. */
public final class MeltValue {
    public final double total;
    public final double perGram;
    public final double perTroyOunce;
    public final double perTroyPound;

    public MeltValue(double total, double perGram, double perTroyOunce, double perTroyPound) {
        this.total = total;
        this.perGram = perGram;
        this.perTroyOunce = perTroyOunce;
        this.perTroyPound = perTroyPound;
    }
}
