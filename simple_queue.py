"""
Problem:
Given a fixed length waiting room of n = 7, calculate:
    1. Average waitingTime
    2. Average response time
    3. Average service time
    4. Average queue length
    5. Amount of dropped customer (if waiting room is full then the next customer from pool is dropped)
"""
import random
import string
from typing import (
    Any,
    Dict,
    List,
)
from collections import deque

FLOAT_PRECISION = 1

def finiteWaitingRoom(): # TO-DO: refactor
    customerAmount = int(input("Amount of customer in pool: "))
    customer: List[Dict[str, Any]] = []
    queue = deque([])
    currentlyServedDepartureTime: List = []
    droppedCustomer: List = []
    waitingTime: float = 0
    serviceTime: float = 0
    responseTime: float = 0
    queueLength: int = 0

    for i in range(customerAmount):
        customer.append({
            'Name': ''.join(random.choices(string.ascii_letters, k = 8)), # for log purposes
            'arrivalRate': round(random.random(), FLOAT_PRECISION),
            'serviceRate': round(random.random(), FLOAT_PRECISION)
        })

        if i != 0 and len(queue) < 7:
            customer[i].update({
                'arrivalTime': round((customer[i-1]['arrivalTime'] + customer[i]['arrivalRate']), FLOAT_PRECISION),
            })
            if customer[i]['arrivalTime'] < currentlyServedDepartureTime[-1]:
                customer[i].update({
                    'waitingTime': round((customer[i-1]['departureTime'] - customer[i]['arrivalTime']), FLOAT_PRECISION)
                })
                customer[i].update({
                    'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                })
                queue.append(customer[i]['departureTime'])
            elif customer[i]['arrivalTime'] >= currentlyServedDepartureTime[-1] :
                if queue:
                    while queue:
                        if queue[0] <= customer[i]['arrivalTime']:
                            currentlyServedDepartureTime.append(queue.popleft())                 
                        else:
                            currentlyServedDepartureTime.append(queue.popleft())
                            break
                    if queue:
                        customer[i].update({
                            'waitingTime': round((queue[-1] - customer[i]['arrivalTime']), FLOAT_PRECISION)
                        })
                        customer[i].update({
                            'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                        })
                        queue.append(customer[i]['departureTime'])    
                    else:
                        if customer[i]['arrivalTime'] >= currentlyServedDepartureTime[-1]: 
                            customer[i].update({
                                'waitingTime': 0
                            })
                            currentlyServedDepartureTime.append(customer[i]['arrivalTime'])
                            customer[i].update({
                                'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                            })
                        else:
                            customer[i].update({
                                'waitingTime': round((currentlyServedDepartureTime[-1] - customer[i]['arrivalTime']), FLOAT_PRECISION)
                            })
                            customer[i].update({
                                'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                            })
                            queue.append(customer[i]['departureTime'])                               
                else:
                    customer[i].update({
                        'waitingTime': 0
                    })
                    customer[i].update({
                        'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                    })
                    currentlyServedDepartureTime.append(customer[i]['departureTime'])          
        elif i != 0 and len(queue) >= 7:
            customer[i].update({
                'arrivalTime': round((customer[i-1]['arrivalTime'] + customer[i]['arrivalRate']), FLOAT_PRECISION),
            })
            if customer[i]['arrivalTime'] >= currentlyServedDepartureTime[-1]:
                while queue:
                    if queue[0] <= customer[i]['arrivalTime']:
                        currentlyServedDepartureTime.append(queue.popleft())                 
                    else:
                        currentlyServedDepartureTime.append(queue.popleft())
                        break
                if queue:
                    customer[i].update({
                        'waitingTime': round((queue[-1] - customer[i]['arrivalTime']), FLOAT_PRECISION)
                    })
                else:
                    customer[i].update({
                        'waitingTime': 0
                    })             
                customer[i].update({
                    'departureTime': round((customer[i]['arrivalTime'] + customer[i]['serviceRate'] + customer[i].get('waitingTime')), FLOAT_PRECISION)
                })
                queue.append(customer[i]['departureTime'])
            else:
                customer[i].update({
                    'Status': 'Dropped'
                })
                droppedCustomer.append(customer[-1]['Name'])
        else:
            customer[i].update({
                'arrivalTime': 0 + customer[i]['arrivalRate'],
                'waitingTime': 0,
                'departureTime': round((customer[i]['arrivalRate'] + customer[i]['serviceRate']), FLOAT_PRECISION)
            })
            currentlyServedDepartureTime.append(customer[i]['departureTime'])

        waitingTime += customer[i].get('waitingTime', 0)
        serviceTime += customer[i]['serviceRate']
        responseTime += customer[i].get('waitingTime', 0) + customer[i]['serviceRate']
        queueLength += len(queue)

        print(f"{i+1}. {customer[i]}")
        print(f"Served customer will depart in: {currentlyServedDepartureTime[-1]}")
        print(f"Queue: {queue} \n")
    
    print(f"Average Waiting Time: {round((waitingTime/customerAmount), FLOAT_PRECISION)}")
    print(f"Average Response Time: {round((responseTime/customerAmount), FLOAT_PRECISION)}")
    print(f"Average Queue Length: {int(queueLength/customerAmount)}")
    print(f"Amount of Dropped Customer: {len(droppedCustomer)}")
    
if __name__ == "__main__":
    finiteWaitingRoom()