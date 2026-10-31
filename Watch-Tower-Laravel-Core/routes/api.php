<?php

use App\Http\Controllers\Api\ChangesController;
use App\Http\Controllers\Api\HealthController;
use App\Http\Controllers\Api\ProgramsController;
use App\Http\Controllers\Api\StatsController;
use App\Http\Controllers\Api\SubdomainsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/health', [HealthController::class, 'index']);

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::prefix('v2.1')->middleware('throttle:120,1')->group(function () {
    Route::get('stats', [StatsController::class, 'index']);
    Route::get('sources', [StatsController::class, 'sources']);

    Route::get('changes/count', [ChangesController::class, 'count']);
    Route::get('changes', [ChangesController::class, 'index']);

    Route::apiResource('programs', ProgramsController::class)
        ->only(['index', 'show', 'store', 'update', 'destroy']);

    Route::apiResource('subdomains', SubdomainsController::class)
        ->only(['index', 'show']);
});
