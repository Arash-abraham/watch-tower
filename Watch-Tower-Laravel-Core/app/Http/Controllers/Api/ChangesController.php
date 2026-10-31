<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\ChangesResource;
use App\Models\Change;
use Illuminate\Http\Request;
use Illuminate\Support\Carbon;

class ChangesController extends Controller
{
    public function index(Request $request)
    {
        $perPage = min(max((int) $request->query('per_page', 25), 1), 100);

        $query = Change::query()
            ->fromSource($request->query('source'))
            ->ofType($request->query('type'))
            ->orderByDesc('detected_at');

        if ($slug = $request->query('program')) {
            $query->where('slug', $slug);
        }

        if ($since = $request->query('since')) {
            try {
                $query->where('detected_at', '>=', Carbon::parse($since));
            } catch (\Throwable) {
                // ignore invalid dates instead of failing the whole request
            }
        }

        if ($search = trim((string) $request->query('q'))) {
            $regex = '/'.preg_quote($search, '/').'/i';
            $query->where(function ($inner) use ($regex) {
                $inner->where('target', 'regex', $regex)
                    ->orWhere('program_name', 'regex', $regex);
            });
        }

        if ($request->has('notified') && $request->query('notified') !== '') {
            $query->where('notified', $request->boolean('notified'));
        }

        return ChangesResource::collection($query->paginate($perPage)->withQueryString());
    }

    public function count(Request $request)
    {
        return response()->json([
            'data' => [
                'total' => Change::count(),
                'last_24h' => Change::where('detected_at', '>=', now()->subDay())->count(),
                'last_7d' => Change::where('detected_at', '>=', now()->subDays(7))->count(),
                'unnotified' => Change::where('notified', false)->count(),
            ],
        ]);
    }
}
