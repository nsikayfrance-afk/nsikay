from channels.generic.websocket import AsyncJsonWebsocketConsumer



class NotificationConsumer(
    AsyncJsonWebsocketConsumer
):


    async def connect(self):

        await self.accept()



    async def receive_json(
        self,
        content
    ):

        await self.send_json({

            "platform":
            "NSIKAY",

            "status":
            "MESSAGE_RECEIVED",

            "data":
            content

        })


