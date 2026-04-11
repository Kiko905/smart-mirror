<?php

namespace App\Http\Controllers\Api;

use App\Models\User;
use Illuminate\Http\Request;
use App\Models\MirrorProfile;
use App\Http\Controllers\Controller;

class MirrorProfileController extends Controller
{
    public function index(User $user)
    {
        $profiles = MirrorProfile::query()
            ->with('layout')
            ->where('user_id', $user->id)
            ->orderByDesc('is_active')
            ->orderBy('id')
            ->get();

        return response()->json([
            'data' => $profiles->map(function (MirrorProfile $profile) {
                return [
                    'id' => $profile->id,
                    'user_id' => $profile->user_id,
                    'profile_name' => $profile->profile_name,
                    'is_active' => $profile->is_active,
                    'has_layout' => $profile->layout !== null,
                ];
            }),
        ]);
    }

    public function store(Request $request, User $user)
    {
        $validated = $request->validate([
            'profile_name' => 'required|string|max:255',
            'is_active' => 'nullable|boolean',
        ]);

        $isActive = (bool) ($validated['is_active'] ?? false);

        if ($isActive) {
            MirrorProfile::query()
                ->where('user_id', $user->id)
                ->update(['is_active' => false]);
        }

        $profile = MirrorProfile::query()->create([
            'user_id' => $user->id,
            'profile_name' => $validated['profile_name'],
            'is_active' => $isActive,
        ]);

        return response()->json([
            'message' => 'Profile created successfully',
            'data' => $profile,
        ], 201);
    }

    public function activate(MirrorProfile $profile)
    {
        MirrorProfile::query()
            ->where('user_id', $profile->user_id)
            ->update(['is_active' => false]);

        $profile->update(['is_active' => true]);

        return response()->json([
            'message' => 'Profile activated successfully',
            'data' => $profile,
        ]);
    }
}
