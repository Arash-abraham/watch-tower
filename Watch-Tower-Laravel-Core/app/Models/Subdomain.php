<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

/**
 * Passive discovery results written by the collector; the API is read-only.
 */
class Subdomain extends Model
{
    protected $connection = 'mongodb';

    protected $collection = 'subdomains';

    public $timestamps = false;

    protected $fillable = [
        'host',
        'program_slug',
        'source',
        'resolved',
        'ip',
        'first_seen_at',
        'last_seen_at',
    ];

    protected $casts = [
        'resolved' => 'boolean',
        'first_seen_at' => 'datetime',
        'last_seen_at' => 'datetime',
    ];
}
