<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\SyncRunResource;
use App\Models\Change;
use App\Models\Program;
use App\Models\SyncRun;
use Illuminate\Support\Facades\DB;

class StatsController extends Controller
{
    public function index()
    {
        $dayAgo = now()->subDay();
        $lastRun = SyncRun::query()->orderByDesc('started_at')->first();

        return response()->json([
            'data' => [
                'programs' => Program::count(),
                'active_programs' => Program::where('active', true)->count(),
                'scopes' => $this->countScopes(),
                'changes' => Change::count(),
                'changes_24h' => Change::where('detected_at', '>=', $dayAgo)->count(),
                'changes_7d' => Change::where('detected_at', '>=', now()->subDays(7))->count(),
                'conflicts' => Program::where('conflicts', '!=', [])->count(),
                'last_run' => $lastRun ? new SyncRunResource($lastRun) : null,
                'sources' => $this->sourceBreakdown(),
                'schedule_interval' => (int) config('watchtower.scan_interval', 1800),
                'notifications' => (array) config('watchtower.notifications', []),
                'generated_at' => now()->toIso8601String(),
            ],
        ]);
    }

    public function sources()
    {
        return response()->json(['data' => $this->sourceBreakdown()]);
    }

    /**
     * Per-source counters used by the dashboard and the "Applications" page.
     */
    private function sourceBreakdown(): array
    {
        $dayAgo = now()->subDay();
        $rows = [];

        foreach ((array) config('watchtower.sources', []) as $source) {
            $latestRun = SyncRun::query()->where('source', $source)->orderByDesc('started_at')->first();

            $rows[] = [
                'source' => $source,
                'programs' => Program::where('source', $source)->count(),
                'active_programs' => Program::where('source', $source)->where('active', true)->count(),
                'changes_24h' => Change::where('source', $source)->where('detected_at', '>=', $dayAgo)->count(),
                'last_run' => $latestRun ? (new SyncRunResource($latestRun))->resolve() : null,
            ];
        }

        return $rows;
    }

    private function countScopes(): int
    {
        try {
            $result = DB::connection('mongodb')
                ->getMongoDB()
                ->selectCollection('programs')
                ->aggregate([
                    ['$match' => ['active' => true]],
                    ['$project' => ['total' => ['$size' => ['$ifNull' => ['$scopes', []]]]]],
                    ['$group' => ['_id' => null, 'sum' => ['$sum' => '$total']]],
                ])
                ->toArray();

            return (int) ($result[0]['sum'] ?? 0);
        } catch (\Throwable) {
            return 0;
        }
    }
}
