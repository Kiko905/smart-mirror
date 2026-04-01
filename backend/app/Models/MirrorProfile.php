<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class MirrorProfile extends Model
{
    protected $fillable = [
        'user_id',
        'profile_name',
        'is_active',
    ];

    public function layout()
    {
        return $this->hasOne(MirrorLayout::class);
    }

    public function user()
    {
        return $this->belongsTo(User::class);
    }
}