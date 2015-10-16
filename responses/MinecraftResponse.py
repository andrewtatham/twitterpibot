from Response import Response
import MyMinecraft
class MinecraftResponse(Response):
    def Condition(args, inboxItem):
        return super(MinecraftResponse, args).Condition(inboxItem) \
            and args.Contains(inboxItem.words, "minecraft")
    def Respond(args, inboxItem):

        mc = MyMinecraft.Connect()

        pPos = mc.player.getTilePos()

   
        mc.setBlocks(pPos.x-1,pPos.y,pPos.z-1,pPos.x+1,pPos.y+2,pPos.z+1,block.STONE)


        mc.player.setPos(pPos.x,pPos.y+3,pPos.z)


        filename = MyMinecraft.TakeScreenshot("temp/mc.png")

