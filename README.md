### DRL Level Generator

##### Uses

1. Unity 2020
1. Python 3.7
1. [ZeroMQ](https://zeromq.org/), it's C# port [NetMQ](https://github.com/zeromq/netmq) 
    and followed [this repo](https://github.com/off99555/Unity3D-Python-Communication) to add
    NetMQ to my Unity project.
    
    1. Copied `.dll`s from `UnityProject/Assets/Plugins` to my own project's `Assets/Plugins`
    1. Followed examples at `UnityProject/Assets/NetMQExample/Scripts/*.cs`
    1. For python:
        1. `pip install pyzmq`
        2. Followed example at `PythonFiles/server.py`