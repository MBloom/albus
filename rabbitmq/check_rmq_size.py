import argparse

from rabbitmq_checker import RabbitMQChecker

parser = argparse.ArgumentParser(description='Process some integers.')
parser.add_argument('queue_name', help='name of the queue to query')
parser.add_argument('--host', default='localhost', 
	help='rabbitmq hostname')

args = parser.parse_args()

RabbitMQChecker(args.host).print_queue_size(args.queue_name)