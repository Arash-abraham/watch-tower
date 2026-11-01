<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use Illuminate\Support\Facades\DB;

class HealthController extends Controller
{
    public function index()
    {
        $mongo = false;
        $error = null;

        try {
            DB::connection('mongodb')->getMongoDB()->command(['ping' => 1]);
            $mongo = true;
        } catch (\Throwable $exception) {
            $error = $exception->getMessage();
        }

        return response()->json(
            [
                'status' => $mongo ? 'ok' : 'degraded',
                'service' => 'watch-tower-api',
                'version' => '2.1',
                'mongo' => $mongo,
                'error' => $error,
                'time' => now()->toIso8601String(),
            ],
            $mongo ? 200 : 503
        );
    }
}
