defaultSelectedFields = ['hitId',
                         'datetime:$date', 
                         'analysis:level',
                         'clientData:ncd',
                         'clientData:tz', 
                         'clientData:plt',
                         'clientData:cntp', 
                         'visitor:headers:User-Agent',
                         'clientData:nt',
                         'clientData:evln',
                         'clientData:dm',
                         'clientData:hls',
                         'clientData:mtp',
                         'clientData:rtt',
                         'clientData:scd',
                         'clientData:flv',
                         'clientData:dpr',
                         'clientData:spd',
                         'clientData:wglv',
                         'clientData:tch',
                         'clientData:vnd',
                         'clientData:ornt',
                         'clientData:ciphers',
                         'visitor:headers:X-HA-Conn-Rate',
                         'visitor:headers:X-SSL-Protocol',
                         'visitor:headers:X-HA-RTT',
                         'visitor:headers:X-HA-RTT-Var',
                         'visitor:headers:X-HA-In-Rate',
                         'visitor:headers:X-HA-Out-Rate',
                         'visitor:headers:X-SSL-Cipher',
]

defaultFieldsLabels = ['id',
                       'datetime',
                       'risk_level',
                       'network_speed',
                       'timezone',
                       'platform',
                       'connection_type',
                       'ua_headers',
                       'nt',
                       'evln',
                       'dm',
                       'hls',
                       'mtp',
                       'rtt',
                       'scd',
                       'flv',
                       'dpr',
                       'spd',
                       'wglv',
                       'tch',
                       'vnd',
                       'ornt',
                       'ciphers',
                       'x-ha-conn-rate',
                       'x-ssl-protocol',
                       'x-ha-rtt',
                       'x-ha-rtt-var',
                       'x-ha-in-rate',
                       'x-ha-out-rate',
                       'x-ssl-Cipher',
]


defaultParsedFields = ['ua_product',
                       'ua_os',
                       'ua_platform',
                       'ua_productV',
                       'midnight_seconds',
                       'nt',
                       'rtt_diff',
                       'rtt_var_ratio',
]

defaultHotencFields = ['platform',
                       'connection_type',
                       'ua_product',
                       'ua_os',
                       'ua_platform',
                       'ua_productV',
                       #                         'nt',
                       'evln',
                       'dm',
                       'hls',
                       'mtp',
                       'rtt',
                       'scd',
                       'flv',
                       'dpr',
                       'spd',
                       'wglv',
                       'tch',
                       'vnd',
                       'ornt',
                       'ciphers',
                       'x-ssl-protocol',
                       'x-ssl-Cipher',
]
