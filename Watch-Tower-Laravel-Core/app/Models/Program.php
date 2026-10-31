<?php

namespace App\Models;

use MongoDB\Laravel\Eloquent\Model;

/**
 * A bounty program (or a locally defined asset set).
 *
 * Documents are written by the Python collector; the API only reads them and
 * allows local CRUD of manually maintained programs.
 */
class Program extends Model
{
    protected $connection = 'mongodb';

    protected $collection = 'programs';

    /** The collector owns created_at / last_update, not Eloquent. */
    public $timestamps = false;

    protected $fillable = [
        'source',
        'slug',
        'program_name',
        'program_url',
        'scopes',
        'outScopes',
        'scope_details',
        'meta',
        'conflicts',
        'active',
        'first_seen_at',
        'last_update',
        'last_synced_at',
    ];

    protected $casts = [
        'scopes' => 'array',
        'outScopes' => 'array',
        'scope_details' => 'array',
        'meta' => 'array',
        'conflicts' => 'array',
        'active' => 'boolean',
        'first_seen_at' => 'datetime',
        'last_update' => 'datetime',
        'last_synced_at' => 'datetime',
    ];

    protected $attributes = [
        'scopes' => [],
        'outScopes' => [],
        'conflicts' => [],
        'active' => true,
    ];

    public function scopeSearch($query, ?string $term)
    {
        $term = trim((string) $term);

        if ($term === '') {
            return $query;
        }

        $regex = '/'.preg_quote($term, '/').'/i';

        return $query->where(function ($inner) use ($regex) {
            $inner->where('program_name', 'regex', $regex)
                ->orWhere('program_url', 'regex', $regex)
                ->orWhere('scopes', 'regex', $regex)
                ->orWhere('outScopes', 'regex', $regex);
        });
    }

    public function scopeFromSource($query, ?string $source)
    {
        return $source ? $query->where('source', $source) : $query;
    }

    public function scopeOnlyActive($query)
    {
        return $query->where('active', true);
    }
}
