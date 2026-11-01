<?php

namespace App\Http\Controllers\Api;

use App\Http\Controllers\Controller;
use App\Http\Requests\ProgramsRequest;
use App\Http\Resources\ProgramsResource;
use App\Models\Program;
use Illuminate\Http\Request;
use Illuminate\Support\Str;

class ProgramsController extends Controller
{
    private const SORTABLE = [
        'name' => 'program_name',
        'updated' => 'last_synced_at',
        'source' => 'source',
    ];

    public function index(Request $request)
    {
        $perPage = min(max((int) $request->query('per_page', 15), 1), 100);
        $sort = self::SORTABLE[$request->query('sort', 'name')] ?? 'program_name';
        $direction = $request->query('direction') === 'desc' ? 'desc' : 'asc';

        $query = Program::query()->fromSource($request->query('source'));
        
        $search = trim((string) $request->query('q', ''));
        
        if ($search !== '') {
            $query->where(function ($q) use ($search) {
                $q->where('program_name', 'like', '%' . $search . '%')
                ->orWhere('slug', 'like', '%' . $search . '%');
            });
        }

        if ($request->has('active') && $request->query('active') !== '') {
            $query->where('active', $request->boolean('active'));
        }

        if ($request->boolean('bounty_only')) {
            $query->where('meta.offers_bounties', true);
        }

        if ($request->boolean('conflicts_only')) {
            $query->where('conflicts', '!=', []);
        }

        $programs = $query->orderBy($sort, $direction)->paginate($perPage)->withQueryString();

        return ProgramsResource::collection($programs);
    }

    public function show(string $id)
    {
        return new ProgramsResource($this->findProgram($id));
    }

    public function store(ProgramsRequest $request)
    {
        $data = $request->validated();
        $slug = Str::slug($data['program_name']);

        if (Program::where('source', 'local')->where('slug', $slug)->exists()) {
            return response()->json(
                ['message' => 'A local program with this name already exists.', 'slug' => $slug],
                409
            );
        }

        $program = Program::create([
            'source' => 'local',
            'slug' => $slug,
            'program_name' => $data['program_name'],
            'program_url' => $data['program_url'] ?? null,
            'scopes' => array_values($data['scopes'] ?? []),
            'outScopes' => array_values($data['out_of_scope'] ?? []),
            'scope_details' => ['in' => [], 'out' => []],
            'meta' => $data['meta'] ?? [],
            'conflicts' => array_values(array_intersect(
                $data['scopes'] ?? [],
                $data['out_of_scope'] ?? []
            )),
            'active' => true,
            'first_seen_at' => now(),
            'last_update' => now(),
            'last_synced_at' => now(),
        ]);

        return (new ProgramsResource($program))->response()->setStatusCode(201);
    }

    public function update(ProgramsRequest $request, string $id)
    {
        $program = $this->findProgram($id);
        $data = $request->validated();

        $program->fill(array_filter([
            'program_name' => $data['program_name'] ?? null,
            'program_url' => $data['program_url'] ?? null,
            'scopes' => isset($data['scopes']) ? array_values($data['scopes']) : null,
            'outScopes' => isset($data['out_of_scope']) ? array_values($data['out_of_scope']) : null,
            'meta' => $data['meta'] ?? null,
        ], static fn ($value) => $value !== null));

        if (isset($data['program_name'])) {
            $program->slug = Str::slug($data['program_name']);
        }

        $program->conflicts = array_values(array_intersect(
            $program->scopes ?? [],
            $program->outScopes ?? []
        ));
        $program->last_update = now();
        $program->save();

        return new ProgramsResource($program);
    }

    public function destroy(string $id)
    {
        $this->findProgram($id)->delete();

        return response()->noContent();
    }

    private function findProgram(string $id): Program
    {
        try {
            return Program::query()->findOrFail($id);
        } catch (\Throwable) {
            abort(404, 'Program not found.');
        }
    }
}
