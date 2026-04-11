<?php

namespace App\Http\Controllers\Api;

use App\Models\User;
use Illuminate\Http\Request;
use App\Models\FaceEncoding;
use App\Http\Controllers\Controller;

class FaceEncodingController extends Controller
{
    public function index(User $user)
    {
        $encodings = FaceEncoding::query()
            ->where('user_id', $user->id)
            ->orderByDesc('id')
            ->get(['id', 'user_id', 'encoding', 'image_path', 'created_at']);

        return response()->json(['data' => $encodings]);
    }

    public function store(Request $request, User $user)
    {
        $validated = $request->validate([
            'encoding' => 'required|array|min:8',
            'encoding.*' => 'numeric',
            'image_path' => 'nullable|string|max:1024',
        ]);

        $record = FaceEncoding::query()->create([
            'user_id' => $user->id,
            'encoding' => $validated['encoding'],
            'image_path' => $validated['image_path'] ?? null,
        ]);

        return response()->json([
            'message' => 'Face encoding saved successfully',
            'data' => $record,
        ], 201);
    }

    public function update(Request $request, FaceEncoding $encoding)
    {
        $validated = $request->validate([
            'encoding' => 'required|array|min:8',
            'encoding.*' => 'numeric',
            'image_path' => 'nullable|string|max:1024',
        ]);

        $encoding->update([
            'encoding' => $validated['encoding'],
            'image_path' => $validated['image_path'] ?? null,
        ]);

        return response()->json([
            'message' => 'Face encoding updated successfully',
            'data' => $encoding,
        ]);
    }

    public function destroy(FaceEncoding $encoding)
    {
        $encoding->delete();

        return response()->json([
            'message' => 'Face encoding removed successfully',
        ]);
    }
}
