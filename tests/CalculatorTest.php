<?php

declare(strict_types=1);

namespace GoldKaratValue\Tests;

use GoldKaratValue\Calculator;
use PHPUnit\Framework\TestCase;

final class CalculatorTest extends TestCase
{
    public function testFourteenKaratRatio(): void
    {
        $this->assertEqualsWithDelta(14.0 / 24.0, Calculator::purityRatio(14.0), 1e-12);
    }

    public function testMeltValueMatchesCentRounding(): void
    {
        $value = Calculator::meltValue(10.0, 'gram', 14.0, 65.0);
        $this->assertSame(37.92, $value['per_gram']);
        $this->assertSame(379.2, $value['total']);
        $this->assertSame(1179.44, $value['per_troy_ounce']);
        $this->assertSame(14153.34, $value['per_troy_pound']);
    }

    public function testTroyOunceConvertsToGrams(): void
    {
        $this->assertEqualsWithDelta(31.1035, Calculator::toGrams(1.0, 'troy_ounce'), 1e-12);
    }

    public function testScrapAppliesDiscount(): void
    {
        $value = Calculator::scrapValue(10.0, 'gram', 14.0, 65.0, 0.85);
        $this->assertSame(379.2, $value['market']);
        $this->assertSame(322.32, $value['scrap']);
    }

    public function testRejectsOutOfRangeKarat(): void
    {
        $this->expectException(\InvalidArgumentException::class);
        Calculator::meltValue(1.0, 'gram', 25.0, 10.0);
    }
}
