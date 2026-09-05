<?php

use App\Http\Controllers\Api\ProgramsController;
use Illuminate\Http\Request;
use Illuminate\Support\Facades\Route;

Route::get('/user', function (Request $request) {
    return $request->user();
})->middleware('auth:sanctum');

Route::prefix('v2.1')->group(function () {
    Route::apiResource('programs', ProgramsController::class);
    Route::apiResource('subdomains', SubdomainsController::class);
});
