<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

/**
 * Public representation of a program.
 *
 * Field names are snake_case on purpose: the Vue app consumes them directly.
 */
class ProgramsResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => (string) $this->id,
            'source' => $this->source,
            'slug' => $this->slug,
            'name' => $this->program_name,
            'url' => $this->program_url,
            'active' => (bool) $this->active,
            'scopes' => $this->scopes ?? [],
            'out_of_scope' => $this->outScopes ?? [],
            'scope_details' => $this->scope_details ?? ['in' => [], 'out' => []],
            'conflicts' => $this->conflicts ?? [],
            'meta' => $this->meta ?? [],
            'first_seen_at' => optional($this->first_seen_at)->toIso8601String(),
            'last_synced_at' => optional($this->last_synced_at)->toIso8601String(),
        ];
    }
}
