<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::connection('mongodb')->create('programs', function (Blueprint $collection) {
            $collection->index('program_name');
            $collection->index('scopes');
            $collection->index('outScopes');
            $collection->timestamps();
        });
    }

    public function down(): void
    {
        Schema::connection('mongodb')->drop('programs');
    }
};