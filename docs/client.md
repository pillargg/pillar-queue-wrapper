::: pillar_queue.client.Queue
    handler: python
    selection: 
        members:
            - __init__
            - __len__
            - receive_message
            - wait_for_message
            - send_message
            - purge
    rendering: 
        show_root_heading: false
        show_source: false