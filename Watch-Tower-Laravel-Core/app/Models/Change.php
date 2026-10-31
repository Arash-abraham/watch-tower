<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

/**
 * One detected scope change (the alert feed).
 */
class Change extends Model
{
    protected $connection = 'mongodb';

    protected $collection = 'changes';

    public $timestamps = false;

    protected $fillable = [
        'source',
        'slug',
        'program_name',
        'type',
        'scope',
        'target',
        'asset_type',
        'detected_at',
        'notified',
        'notified_at',
    ];

    protected $casts = [
        'detected_at' => 'datetime',
        'notified_at' => 'datetime',
        'notified' => 'boolean',
    ];

    public function scopeFromSource($query, ?string $source)
    {
        return $source ? $query->where('source', $source) : $query;
    }

    public function scopeOfType($query, ?string $type)
    {
        return $type ? $query->where('type', $type) : $query;
    }
}
