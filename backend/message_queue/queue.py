from typing import Callable, Dict, Any, List
from collections import deque
import uuid
import time

class MessageQueue:
    def __init__(self):
        self.queues: Dict[str, deque] = {}
        self.handlers: Dict[str, List[Callable]] = {}
    
    def create_queue(self, queue_name: str) -> None:
        if queue_name not in self.queues:
            self.queues[queue_name] = deque()
            self.handlers[queue_name] = []
    
    def publish(self, queue_name: str, message: Dict[str, Any]) -> None:
        if queue_name not in self.queues:
            self.create_queue(queue_name)
        
        if 'id' not in message:
            message['id'] = str(uuid.uuid4())
        if 'timestamp' not in message:
            message['timestamp'] = time.time()
        
        self.queues[queue_name].append(message)
        
        for handler in self.handlers[queue_name]:
            try:
                handler(message)
            except Exception as e:
                print(f"Error processing message: {e}")
    
    def subscribe(self, queue_name: str, handler: Callable) -> None:
        if queue_name not in self.handlers:
            self.create_queue(queue_name)
        self.handlers[queue_name].append(handler)
    
    def consume(self, queue_name: str) -> Dict[str, Any]:
        if queue_name not in self.queues or not self.queues[queue_name]:
            return None
        return self.queues[queue_name].popleft()

message_queue = MessageQueue()

message_queue.create_queue("payments")