from twitterpibot.twitter.topics import Daily, Annual, Celebrity, Politics, Sport, Entertainment

_topics = []
_topics.extend(Daily.get())
_topics.extend(Annual.get())
_topics.extend(Politics.get())
_topics.extend(Celebrity.get())
_topics.extend(Sport.get())
_topics.extend(Entertainment.get())


def get_topics(text):
    results = map(lambda topic: topic.condition(text), _topics)
    matching_topics = list(filter(_has_matches, results))
    if len(matching_topics) <= 3:
        return sorted(matching_topics, key=_score, reverse=True)
    else:
        return None


def _has_matches(result):
    return result and ("definite_matches" in result and result["definite_matches"]
                       or "possible_matches" in result and result["possible_matches"])


def _score(result):
    score = 0
    if "definite_matches" in result:
        score += len(result["definite_matches"]) * 10
    if "possible_matches" in result:
        score += len(result["possible_matches"])
    return score
