class Event:
  def __init__(self, event):
    """
    :param event: JSON response from FTC API for that event
    """
    from events import create_team_list

    self.event_code = event['code']
    self.name = event['name']

    # Location Info
    self.country = event['country']
    self.state_province = event['stateprov']
    self.city = event['city']

    self.dateStart = event['dateStart']
    self.dateEnd = event['dateEnd']

    self.team_list = create_team_list(event['code'])

  def __repr__(self):
    return f"{self.event_code, self.name}"
