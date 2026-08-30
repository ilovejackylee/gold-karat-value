package io.github.ilovejackylee.goldkaratvalue;

/** Melt value plus a buyer-style scrap estimate. */
public final class ScrapValue {
    public final double market;
    public final double scrap;

    public ScrapValue(double market, double scrap) {
        this.market = market;
        this.scrap = scrap;
    }
}
