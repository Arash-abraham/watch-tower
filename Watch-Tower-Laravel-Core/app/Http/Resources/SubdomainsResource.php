<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class SubdomainsResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => (string) $this->id,
            'host' => $this->host,
            'program' => $this->program_slug,
            'source' => $this->source,
            'resolved' => (bool) $this->resolved,
            'ip' => $this->ip,
            'first_seen_at' => optional($this->first_seen_at)->toIso8601String(),
            'last_seen_at' => optional($this->last_seen_at)->toIso8601String(),
        ];
    }
}
