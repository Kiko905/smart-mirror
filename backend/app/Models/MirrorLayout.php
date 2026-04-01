<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class MirrorLayout extends Model
{
    protected $fillable = [
        'mirror_profile_id',
        'layout_json',
    ];

    protected $casts = [
        'layout_json' => 'array',
    ];

    public function profile()
    {
        return $this->belongsTo(MirrorProfile::class, 'mirror_profile_id');
    }
}