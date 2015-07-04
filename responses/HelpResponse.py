from Response import Response

class HelpResponse(Response):
    def Condition(args, inboxItem):
        return super(HelpResponse,args).Condition(inboxItem) and args.Contains(inboxItem.words, "helptest")

    def Respond(args, inboxItem):
        helpText = 'blah blah help'

        return args.ReplyWith(
            inboxItem=inboxItem, 
            text=helpText)
