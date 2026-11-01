<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::connection('mongodb')->create('programs', function (Blueprint $collection) {
            $collection->unique(['source', 'slug']);
            $collection->index('scopes');
            $collection->index('last_synced_at');
        });
    }

    public function down(): void
    {
        Schema::connection('mongodb')->drop('programs');
    }
};
