import messagehandler
import json

responses = ["Ni no Kuni 2",
             "FF X",
             "Devil May Cry",
             "Dragon Quest XI",
             "Gravity Rush 2",
             "Paper Mario: Color Splash"]

try:
    with open('data/votes.json', 'r') as f:
        votes = json.load(f)
except:
    votes = {}


@messagehandler.register("twitch", "!choices")
def choices(bot, sent_by, msg_text, channel=None):
    bot.write_to_chat(', '.join(["{} - {}".format(i, r) for i, r in enumerate(responses)]), channel)


@messagehandler.register("twitch", "!vote")
def vote(bot, sent_by, msg_text, channel=None):
    try:
        extra_command = msg_text.split(' ', 1)[1]
        try:
            extra_command_as_int = int(extra_command)
        except ValueError:
            extra_command_as_int = -1
        for response in responses:
            if response.lower() in extra_command.lower():
                votes[sent_by] = response
                break
            elif len(responses) > extra_command_as_int >= 0:
                votes[sent_by] = responses[extra_command_as_int]
                break
        with open('data/votes.json', 'w+') as f:
            f.write(json.dumps(votes))
    except IndexError:
        pass
