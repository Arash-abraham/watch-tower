<?php

namespace App\Http\Resources;

use Illuminate\Http\Request;
use Illuminate\Http\Resources\Json\JsonResource;

class ChangesResource extends JsonResource
{
    public function toArray(Request $request): array
    {
        return [
            'id' => (string) $this->id,
            'source' => $this->source,
            'program' => [
                'slug' => $this->slug,
                'name' => $this->program_name,
            ],
            'type' => $this->type,
            'scope' => $this->scope,
            'target' => $this->target,
            'asset_type' => $this->asset_type,
            'detected_at' => optional($this->detected_at)->toIso8601String(),
            'notified' => (bool) $this->notified,
        ];
    }
}
