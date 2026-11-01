<?php

return [

    /*
    |--------------------------------------------------------------------------
    | Monitored sources
    |--------------------------------------------------------------------------
    |
    | The collector writes one document per program/source. Keep this list in
    | sync with SOURCES in Watch-Tower-Python-Core/.env ("local" holds the
    | manually maintained programs).
    |
    */

    'sources' => array_values(array_filter(array_map(
        'trim',
        explode(',', (string) env('WATCHTOWER_SOURCES', 'bugcrowd,hackerone,yeswehack,intigriti,local'))
    ))),

    /*
    |--------------------------------------------------------------------------
    | Collector cadence (seconds)
    |--------------------------------------------------------------------------
    |
    | Displayed by the dashboard; the actual scheduling happens in the
    | collector container (monitor.py --watch).
    |
    */

    'scan_interval' => (int) env('WATCHTOWER_SCAN_INTERVAL', 1800),

    /*
    |--------------------------------------------------------------------------
    | Notification channels
    |--------------------------------------------------------------------------
    |
    | Only used for display; sending happens in the Python core.
    |
    */

    'notifications' => [
        'telegram' => (bool) env('WATCHTOWER_TELEGRAM_ENABLED', false),
        'discord' => (bool) env('WATCHTOWER_DISCORD_ENABLED', false),
    ],
];
