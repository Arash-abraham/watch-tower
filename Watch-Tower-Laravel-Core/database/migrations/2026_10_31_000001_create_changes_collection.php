<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::connection('mongodb')->create('changes', function (Blueprint $collection) {
            $collection->index('detected_at');
            $collection->index(['source', 'detected_at']);
            $collection->index('notified');
        });
    }

    public function down(): void
    {
        Schema::connection('mongodb')->drop('changes');
    }
};
