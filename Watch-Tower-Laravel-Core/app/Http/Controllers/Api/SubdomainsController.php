<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Resources\SubdomainsResource;
use App\Models\Subdomain;
use Illuminate\Http\Request;

/**
 * Read-only API for manually collected subdomain discovery results.
 */
class SubdomainsController extends Controller
{
    public function index(Request $request)
    {
        $filters = $request->validate([
            'source' => ['nullable', 'string', 'max:64'],
            'program' => ['nullable', 'string', 'max:255'],
            'q' => ['nullable', 'string', 'max:253'],
            'provider' => ['nullable', 'string', 'regex:/\A[a-z0-9][a-z0-9_-]{0,63}\z/'],
        ]);
        $perPage = min(max((int) $request->query('per_page', 25), 1), 100);

        $query = Subdomain::query()->orderByDesc('last_seen_at')->orderBy('host');
        if (! isset($filters['source'], $filters['program'])) {
            $query->orderBy('source')->orderBy('program_slug');
        }

        if (isset($filters['source'])) {
            $query->where('source', $filters['source']);
        }

        if (isset($filters['program'])) {
            $query->where('program_slug', $filters['program']);
        }

        $search = trim($filters['q'] ?? '');
        if ($search !== '') {
            $query->where('host', 'regex', '/'.preg_quote($search, '/').'/i');
        }

        if (isset($filters['provider'])) {
            $query->whereNotNull('observations.'.$filters['provider']);
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
