::: pillar_queue.client.Queue
    handler: python
    selection: 
        members:
            - __init__
            - __len__
            - __getitem__
            - __setitem__
            - __delitem__
            - receive_message
            - receive_messages
            - wait_for_message
            - send_message
            - purge
    rendering: 
        show_root_heading: false
        show_source: false