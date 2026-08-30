<?php

declare(strict_types=1);

namespace GoldKaratValue;

final class Calculator
{
    public const GRAMS_PER_TROY_OUNCE = 31.1035;
    public const GRAMS_PER_PENNYWEIGHT = 1.55517384;
    public const GRAMS_PER_TROY_POUND = 373.242;

    private const WEIGHT_TO_GRAMS = [
        'gram' => 1.0,
        'pennyweight' => self::GRAMS_PER_PENNYWEIGHT,
        'troy_ounce' => self::GRAMS_PER_TROY_OUNCE,
        'troy_pound' => self::GRAMS_PER_TROY_POUND,
        'kilogram' => 1000.0,
    ];

    public static function purityRatio(float $karat): float
    {
        if (!is_finite($karat) || $karat < 0.0 || $karat > 24.0) {
            throw new \InvalidArgumentException('karat must be between 0 and 24');
        }

        return $karat / 24.0;
    }

    public static function toGrams(float $weight, string $unit): float
    {
        if (!is_finite($weight) || $weight < 0.0) {
            throw new \InvalidArgumentException('weight must be finite and non-negative');
        }

        if (!isset(self::WEIGHT_TO_GRAMS[$unit])) {
            throw new \InvalidArgumentException('unknown unit: ' . $unit);
        }

        return $weight * self::WEIGHT_TO_GRAMS[$unit];
    }

    public static function roundCents(float $amount): float
    {
        return round($amount * 100.0) / 100.0;
    }

    /**
     * @return array{total: float, per_gram: float, per_troy_ounce: float, per_troy_pound: float}
     */
    public static function meltValue(float $weight, string $unit, float $karat, float $price24kPerGram): array
    {
        if (!is_finite($price24kPerGram) || $price24kPerGram < 0.0) {
            throw new \InvalidArgumentException('price must be finite and non-negative');
        }

        $grams = self::toGrams($weight, $unit);
        $perGram = self::roundCents($price24kPerGram * self::purityRatio($karat));

        return [
            'total' => self::roundCents($grams * $perGram),
            'per_gram' => $perGram,
            'per_troy_ounce' => self::roundCents($perGram * self::GRAMS_PER_TROY_OUNCE),
            'per_troy_pound' => self::roundCents($perGram * self::GRAMS_PER_TROY_POUND),
        ];
    }

    /**
     * @return array{market: float, scrap: float}
     */
    public static function scrapValue(
        float $weight,
        string $unit,
        float $karat,
        float $price24kPerGram,
        float $discount
    ): array {
        if (!is_finite($discount) || $discount < 0.0 || $discount > 1.0) {
            throw new \InvalidArgumentException('discount must be between 0 and 1');
        }

        $melt = self::meltValue($weight, $unit, $karat, $price24kPerGram);

        return [
            'market' => $melt['total'],
            'scrap' => self::roundCents($melt['total'] * $discount),
        ];
    }
}
