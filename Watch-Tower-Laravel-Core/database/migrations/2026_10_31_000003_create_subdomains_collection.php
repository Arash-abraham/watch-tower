<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::connection('mongodb')->create('subdomains', function (Blueprint $collection) {
            $collection->unique(['source', 'program_slug', 'host']);
            $collection->index('program_slug');
        });
    }

    public function down(): void
    {
        Schema::connection('mongodb')->drop('subdomains');
    }
};
