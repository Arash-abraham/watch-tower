<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\SubdomainsResource;
use App\Models\Subdomain;
use Illuminate\Http\Request;

/**
 * Read-only for now: the collector will populate this collection once the
 * asset-discovery monitors are enabled.
 */
class SubdomainsController extends Controller
{
    public function index(Request $request)
    {
        $perPage = min(max((int) $request->query('per_page', 25), 1), 100);

        $query = Subdomain::query()->orderByDesc('last_seen_at');

        if ($source = $request->query('source')) {
            $query->where('source', $source);
        }

        if ($slug = $request->query('program')) {
            $query->where('program_slug', $slug);
        }

        if ($search = trim((string) $request->query('q'))) {
            $query->where('host', 'regex', '/'.preg_quote($search, '/').'/i');
        }

        return SubdomainsResource::collection($query->paginate($perPage)->withQueryString());
    }

    public function show(string $id)
    {
        try {
            $subdomain = Subdomain::query()->findOrFail($id);
        } catch (\Throwable) {
            abort(404, 'Subdomain not found.');
        }

        return new SubdomainsResource($subdomain);
    }
}
