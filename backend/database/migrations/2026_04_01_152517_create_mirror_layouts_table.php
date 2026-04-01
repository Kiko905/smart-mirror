<?php

use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration {
    public function up(): void
    {
        Schema::create('mirror_layouts', function (Blueprint $table) {
            $table->id();
            $table->foreignId('mirror_profile_id')->constrained()->onDelete('cascade');
            $table->json('layout_json');
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists('mirror_layouts');
    }
};