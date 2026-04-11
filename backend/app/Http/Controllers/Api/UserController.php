<?php

namespace App\Http\Controllers\Api;

use App\Models\User;
use Illuminate\Http\Request;
use App\Http\Controllers\Controller;

class UserController extends Controller
{
    public function index()
    {
        $users = User::query()
            ->withCount('faceEncodings')
            ->orderBy('id')
            ->get()
            ->map(function (User $user) {
                return [
                    'id' => $user->id,
                    'name' => $user->name,
                    'email' => $user->email,
                    'has_face_encoding' => $user->face_encodings_count > 0,
                    'voice_enabled' => (bool) config('services.voice.enabled', false),
                    'voice_mock_mode' => (bool) config('services.voice.mock_mode', true),
                ];
            });

        return response()->json(['data' => $users]);
    }

    public function show(User $user)
    {
        return response()->json([
            'data' => [
                'id' => $user->id,
                'name' => $user->name,
                'email' => $user->email,
                'has_face_encoding' => $user->faceEncodings()->exists(),
                'voice_enabled' => (bool) config('services.voice.enabled', false),
                'voice_mock_mode' => (bool) config('services.voice.mock_mode', true),
            ],
        ]);
    }

    public function store(Request $request)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|max:255|unique:users,email',
        ]);

        $user = User::query()->create([
            'name' => $validated['name'],
            'email' => $validated['email'],
            'password' => 'mirror-admin',
        ]);

        return response()->json([
            'message' => 'User created successfully',
            'data' => $user,
        ], 201);
    }

    public function update(Request $request, User $user)
    {
        $validated = $request->validate([
            'name' => 'required|string|max:255',
            'email' => 'required|email|max:255|unique:users,email,' . $user->id,
        ]);

        $user->update($validated);

        return response()->json([
            'message' => 'User updated successfully',
            'data' => $user,
        ]);
    }
}
