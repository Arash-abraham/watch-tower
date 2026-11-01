<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

/**
 * One collector execution, written by the Python core.
 */
class SyncRun extends Model
{
    protected $connection = 'mongodb';

    protected $collection = 'sync_runs';

    public $timestamps = false;

    protected $fillable = [
        'source',
        'started_at',
        'finished_at',
        'duration_ms',
        'status',
        'error',
        'stats',
    ];

    protected $casts = [
        'started_at' => 'datetime',
        'finished_at' => 'datetime',
        'stats' => 'array',
        'duration_ms' => 'integer',
    ];
}
