[Unit]
Description=Outgoing Chatmail Postfix before queue filter

[Service]
ExecStart={execpath} {config_path} outgoing
Restart=always
RestartSec=5
WatchdogSec=3600
WatchdogSignal=SIGKILL
User=vmail

[Install]
WantedBy=multi-user.target
