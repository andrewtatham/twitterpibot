from Response import Response
from MyMinecraft import MyMinecraft
class MinecraftResponse(Response):
    def Condition(args, inboxItem):
        return super(MinecraftResponse, args).Condition(inboxItem) \
            and args.Contains(inboxItem.words, "minecraft")
    def Respond(args, inboxItem):



        mc = MyMinecraft()
        filename = mc.foo()
        args.context.Upl
        return super(MinecraftResponse, args).Respond(inboxItem)
