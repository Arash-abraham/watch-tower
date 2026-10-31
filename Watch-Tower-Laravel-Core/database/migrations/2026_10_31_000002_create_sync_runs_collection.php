<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::connection('mongodb')->create('sync_runs', function (Blueprint $collection) {
            $collection->index('started_at');
            $collection->index('source');
        });
    }

    public function down(): void
    {
        Schema::connection('mongodb')->drop('sync_runs');
    }
};
