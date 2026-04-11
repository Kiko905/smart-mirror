<?php

namespace App\Http\Controllers\Api;

use App\Models\User;
use App\Http\Controllers\Controller;
use App\Services\MirrorConfigService;

class SyncController extends Controller
{
    public function __construct(private MirrorConfigService $mirrorConfigService)
    {
    }

    public function userConfig(User $user)
    {
        return response()->json([
            'message' => 'Sync payload generated',
            'data' => $this->mirrorConfigService->getActiveConfigForUser($user->id),
        ]);
    }
}
