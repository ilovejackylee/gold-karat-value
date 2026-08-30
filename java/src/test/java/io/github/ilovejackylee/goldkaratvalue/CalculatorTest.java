package io.github.ilovejackylee.goldkaratvalue;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.assertEquals;
import static org.junit.jupiter.api.Assertions.assertThrows;

class CalculatorTest {
    @Test
    void fourteenKaratRatio() {
        assertEquals(14.0 / 24.0, Calculator.purityRatio(14), 1e-12);
    }

    @Test
    void meltValueMatchesCentRounding() {
        MeltValue value = Calculator.meltValue(10, WeightUnit.GRAM, 14, 65);
        assertEquals(37.92, value.perGram, 1e-9);
        assertEquals(379.20, value.total, 1e-9);
        assertEquals(1179.44, value.perTroyOunce, 1e-9);
        assertEquals(14153.34, value.perTroyPound, 1e-9);
    }

    @Test
    void troyOunceConvertsToGrams() {
        assertEquals(31.1035, Calculator.toGrams(1, WeightUnit.TROY_OUNCE), 1e-12);
    }

    @Test
    void scrapAppliesDiscount() {
        ScrapValue value = Calculator.scrapValue(10, WeightUnit.GRAM, 14, 65, 0.85);
        assertEquals(379.20, value.market, 1e-9);
        assertEquals(322.32, value.scrap, 1e-9);
    }

    @Test
    void rejectsOutOfRangeKarat() {
        CalcException ex = assertThrows(
                CalcException.class,
                () -> Calculator.meltValue(1, WeightUnit.GRAM, 25, 10));
        assertEquals(CalcError.INVALID_KARAT, ex.getError());
    }
}
