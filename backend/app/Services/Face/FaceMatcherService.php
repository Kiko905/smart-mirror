<?php

namespace App\Services\Face;

use App\Models\FaceEncoding;
use Illuminate\Support\Collection;

class FaceMatcherService
{
    /**
     * @return array{encoding: FaceEncoding, distance: float}|null
     */
    public function findBestMatch(array $probeEncoding, Collection $storedEncodings, float $threshold): ?array
    {
        $probe = $this->normalizeEncoding($probeEncoding);

        $best = null;

        foreach ($storedEncodings as $candidateEncoding) {
            $candidate = $this->normalizeEncoding($candidateEncoding->encoding ?? []);
            $distance = $this->euclideanDistance($probe, $candidate);

            if ($best === null || $distance < $best['distance']) {
                $best = [
                    'encoding' => $candidateEncoding,
                    'distance' => $distance,
                ];
            }
        }

        if ($best === null || $best['distance'] > $threshold) {
            return null;
        }

        return $best;
    }

    private function normalizeEncoding(array $encoding): array
    {
        return array_values(array_map(static fn ($value) => (float) $value, $encoding));
    }

    private function euclideanDistance(array $probe, array $candidate): float
    {
        if (count($probe) === 0 || count($probe) !== count($candidate)) {
            return INF;
        }

        $sum = 0.0;

        foreach ($probe as $index => $value) {
            $diff = $value - $candidate[$index];
            $sum += $diff * $diff;
        }

        return sqrt($sum);
    }
}
