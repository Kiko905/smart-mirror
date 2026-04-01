<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class FaceEncoding extends Model
{
    protected $fillable = [
        'user_id',
        'encoding',
        'image_path',
    ];

    protected $casts = [
        'encoding' => 'array',
    ];

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}