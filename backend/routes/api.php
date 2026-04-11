<?php

use Illuminate\Support\Facades\Route;
use App\Http\Controllers\Api\UserController;
use App\Http\Controllers\Api\SyncController;
use App\Http\Controllers\Api\FaceEncodingController;
use App\Http\Controllers\Api\MirrorLayoutController;
use App\Http\Controllers\Api\MirrorProfileController;
use App\Http\Controllers\Api\FaceRecognitionController;

Route::get('/users', [UserController::class, 'index']);
Route::post('/users', [UserController::class, 'store']);
Route::get('/users/{user}', [UserController::class, 'show']);
Route::put('/users/{user}', [UserController::class, 'update']);

Route::get('/users/{user}/mirror-profiles', [MirrorProfileController::class, 'index']);
Route::post('/users/{user}/mirror-profiles', [MirrorProfileController::class, 'store']);
Route::patch('/mirror-profiles/{profile}/activate', [MirrorProfileController::class, 'activate']);

Route::get('/mirror-layout/{user}', [MirrorLayoutController::class, 'show']);
Route::post('/mirror-layout/{user}', [MirrorLayoutController::class, 'store']);

Route::get('/users/{user}/face-encodings', [FaceEncodingController::class, 'index']);
Route::post('/users/{user}/face-encodings', [FaceEncodingController::class, 'store']);
Route::put('/face-encodings/{encoding}', [FaceEncodingController::class, 'update']);
Route::delete('/face-encodings/{encoding}', [FaceEncodingController::class, 'destroy']);

Route::post('/face-recognition/match', [FaceRecognitionController::class, 'match']);
Route::get('/sync/config/{user}', [SyncController::class, 'userConfig']);