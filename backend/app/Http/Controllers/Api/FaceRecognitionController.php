<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Http\Request;

class FaceRecognitionController extends Controller
{
    public function match(Request $request)
    {
        $validated = $request->validate([
            'user_id' => 'required|integer'
        ]);

        return response()->json([
            'message' => 'Face matched',
            'user_id' => $validated['user_id']
        ]);
    }
}