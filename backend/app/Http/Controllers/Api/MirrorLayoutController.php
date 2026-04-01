<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Models\MirrorLayout;
use App\Models\MirrorProfile;
use Illuminate\Http\Request;

class MirrorLayoutController extends Controller
{
    public function show($user_id)
    {
        $profile = MirrorProfile::with('layout')
            ->where('user_id', $user_id)
            ->where('is_active', true)
            ->first();

        if (!$profile || !$profile->layout) {
            return response()->json([
                'error' => 'Profile or layout not found'
            ], 404);
        }

        return response()->json([
            'user_id' => $user_id,
            'profile_name' => $profile->profile_name,
            'layout' => $profile->layout->layout_json
        ]);
    }

    public function store(Request $request, $user_id)
    {
        $validated = $request->validate([
            'profile_name' => 'required|string|max:255',
            'layout' => 'required|array'
        ]);

        $profile = MirrorProfile::firstOrCreate(
            [
                'user_id' => $user_id,
                'is_active' => true
            ],
            [
                'profile_name' => $validated['profile_name']
            ]
        );

        $layout = MirrorLayout::updateOrCreate(
            [
                'mirror_profile_id' => $profile->id
            ],
            [
                'layout_json' => $validated['layout']
            ]
        );

        return response()->json([
            'message' => 'Layout saved successfully',
            'profile' => $profile,
            'layout' => $layout
        ]);
    }
}