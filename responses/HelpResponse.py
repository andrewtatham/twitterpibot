from Response import Response

class HelpResponse(Response):
    def Condition(args, inboxItem):
        return super(HelpResponse,args).Condition(inboxItem) and args.Contains(inboxItem.words, "helptest")

    def Respond(args, inboxItem):
        helpText = 'blah blah help'

        return super(HelpResponse,args).ReplyWith(inboxItem, helpText)

    def Contains(args, list, item):
        if list is not None:
            for listItem in list:
                if listItem.lower() == item.lower():
                    return True

        return False;