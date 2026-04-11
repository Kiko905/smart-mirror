<?php

namespace App\Services;

use App\Models\User;
use App\Models\MirrorProfile;

class MirrorConfigService
{
    public function getActiveConfigForUser(int $userId): array
    {
        $user = User::query()->findOrFail($userId);

        $profile = MirrorProfile::query()
            ->with('layout')
            ->where('user_id', $userId)
            ->where('is_active', true)
            ->first();

        $layout = $profile?->layout?->layout_json ?? [];
        $layoutLastUpdated = $profile?->layout?->updated_at?->toISOString();

        $moduleStatus = [
            'face_configured' => $user->faceEncodings()->exists(),
            'voice_enabled' => (bool) config('services.voice.enabled', false),
            'voice_mock_mode' => (bool) config('services.voice.mock_mode', true),
        ];

        return [
            'user' => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
            ],
            'profile' => [
                'id' => $profile?->id,
                'profile_name' => $profile?->profile_name,
                'is_active' => $profile?->is_active ?? false,
            ],
            'layout' => $layout,
            'module_status' => $moduleStatus,
            'sync_token' => sha1(json_encode($layout) . '|' . $layoutLastUpdated . '|' . $user->id),
            'updated_at' => $layoutLastUpdated,
        ];
    }
}
