<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Cross-Origin Resource Sharing
    |--------------------------------------------------------------------------
    |
    | The Vue app runs on its own origin (Vite dev server or nginx) and talks
    | to this API. Set FRONTEND_URL to restrict access; "*" keeps local
    | development frictionless (credentials are not used).
    |
    */

    'paths' => ['api/*', 'sanctum/csrf-cookie'],

    'allowed_methods' => ['*'],

    'allowed_origins' => array_filter(array_map(
        'trim',
        explode(',', (string) env('FRONTEND_URL', '*'))
    )),

    'allowed_origins_patterns' => [],

    'allowed_headers' => ['*'],

    'exposed_headers' => [],

    'max_age' => 3600,

    'supports_credentials' => false,

];
