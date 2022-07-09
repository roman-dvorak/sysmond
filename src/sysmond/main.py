import asyncio
import tornado.web
import json
from rrmngmnt import Host, RootUser


data = [
{
    "service": "mongod",
    "name": "localhost_mongod",
    "default_state": "running",
    "host": {
        "ip": "localhost",
        "pass": "heslo"
    }
},
{
    "service": "lxc",
    "name": "localhost_lxc",
    "default_state": "running",
    "host": {
        "ip": "localhost",
        "pass": "heslo"
    }
}


]


def method_name(obj):
    print("Nastal problem", obj)
    data = {
            '__class__': obj.__class__.__name__,
            '__module__': obj.__module__
           }
    data.update(obj.__name__)
    return data

def update_configs():
    print(data)
    for service in data:
        if not 'context' in service:
            service['context'] = {}
            service['status'] = {}
            service['context']['host'] = Host("localhost")
            service['context']['host'].users.append(RootUser('heslo'))
            service['context']['service'] = service['context']['host'].service(service['service'])

        service['status']['state'] = service['context']['service'].status()



class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("templates/home.hbs")

class DataHandler(tornado.web.RequestHandler):
    def get(self):
        print(data)
        self.write(json.dumps(data, check_circular=False, default=lambda o: '<not serializable>'))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
        (r"/data", DataHandler),
    ],
    debug=True)

async def main():
    app = make_app()
    app.listen(8888)

    some_time_period = 5000
    tornado.ioloop.PeriodicCallback(update_configs, some_time_period).start()


    #tornado.ioloop.IOLoop.instance().start()

    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
