<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class SyncRunResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => (string) $this->id,
            'source' => $this->source,
            'status' => $this->status,
            'started_at' => optional($this->started_at)->toIso8601String(),
            'finished_at' => optional($this->finished_at)->toIso8601String(),
            'duration_ms' => (int) $this->duration_ms,
            'stats' => $this->stats ?? [],
            'error' => $this->error,
        ];
    }
}
