import pika

class RabbitMQChecker:

    def __init__(self, hostname):
        self.hostname = hostname
        self.connection = None

    def print_queue_size(self, name):
        self.__connect()
        size = self.__get_queue_size(name)
        self.__close_connection()

    def __connect(self):
        try:
            credentials = pika.PlainCredentials('guest', 'guest')
            parameters = pika.ConnectionParameters(self.hostname,
                                       5672,
                                       '/',
                                       credentials)
            self.connection = pika.BlockingConnection(parameters)
        except pika.exceptions.ConnectionClosed as e:
            print "Could not connect to rabbitmq at {}".format(self.hostname)

    def __get_queue_size(self, name):
        if self.connection:
            channel = self.connection.channel()
            try:
                queue = channel.queue_declare(queue=name, passive=True)
                print "Queue '{}' has {} messages".format(
                    name, queue.method.message_count)
            except pika.exceptions.ChannelClosed as e:
                print "Queue '{}' does not exist".format(name)

    def __close_connection(self):
        if self.connection:
            self.connection.close()

# Usage
# if __name__ == "__main__":
#     RabbitMQChecker('localhost').print_queue_size('test')