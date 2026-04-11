<?php

namespace App\Http\Controllers\Api;

use App\Models\User;
use App\Models\FaceEncoding;
use App\Http\Controllers\Controller;
use Illuminate\Http\Request;
use App\Services\Face\FaceMatcherService;
use App\Services\MirrorConfigService;

class FaceRecognitionController extends Controller
{
    public function __construct(
        private FaceMatcherService $matcher,
        private MirrorConfigService $mirrorConfigService
    ) {
    }

    public function match(Request $request)
    {
        $validated = $request->validate([
            'probe_encoding' => 'nullable|array|min:8',
            'probe_encoding.*' => 'numeric',
            'threshold' => 'nullable|numeric|min:0|max:10',
            'use_mock' => 'nullable|boolean',
            'mock_user_id' => 'nullable|integer|exists:users,id',
        ]);

        $useMock = (bool) ($validated['use_mock'] ?? config('services.face.mock_mode'));
        $threshold = (float) ($validated['threshold'] ?? config('services.face.match_threshold', 0.6));

        if ($useMock) {
            $mockUserId = $validated['mock_user_id'] ?? User::query()->orderBy('id')->value('id');

            if (!$mockUserId) {
                return response()->json([
                    'matched' => false,
                    'message' => 'No user available for mock recognition',
                ], 404);
            }

            return response()->json([
                'matched' => true,
                'is_mock' => true,
                'user_id' => (int) $mockUserId,
                'confidence_distance' => 0.0,
                'active_config' => $this->mirrorConfigService->getActiveConfigForUser((int) $mockUserId),
            ]);
        }

        if (!isset($validated['probe_encoding'])) {
            return response()->json([
                'matched' => false,
                'message' => 'probe_encoding is required when mock mode is disabled',
            ], 422);
        }

        $encodings = FaceEncoding::query()->with('user')->get();
        $bestMatch = $this->matcher->findBestMatch($validated['probe_encoding'], $encodings, $threshold);

        if (!$bestMatch) {
            return response()->json([
                'matched' => false,
                'message' => 'No face encoding matched threshold',
            ], 404);
        }

        /** @var FaceEncoding $encoding */
        $encoding = $bestMatch['encoding'];

        return response()->json([
            'matched' => true,
            'is_mock' => false,
            'user_id' => $encoding->user_id,
            'face_encoding_id' => $encoding->id,
            'confidence_distance' => $bestMatch['distance'],
            'active_config' => $this->mirrorConfigService->getActiveConfigForUser((int) $encoding->user_id),
        ]);
    }
}