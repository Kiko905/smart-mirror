<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\MirrorLayoutController;

Route::get('/mirror-layout/{user}', [MirrorLayoutController::class, 'show']);
Route::post('/mirror-layout/{user}', [MirrorLayoutController::class, 'store']);