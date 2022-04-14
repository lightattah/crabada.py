"""
Define global configuration variables from reading the
environment
"""

from src.common.exceptions import MissingConfig
from src.common.types import (
    ConfigTeam,
    ConfigUser,
)
from src.common.dotenv import getenv, parseInt, parsePercentage
from typing import Any, Dict, List
from src.helpers.config import parseTeamConfig, parseUserConfig

#################
# Users config
#################

users: List[ConfigUser] = []
userNumber = 1
while getenv(f"USER_{userNumber}_PRIVATE_KEY"):
    # Parse config of user's teams
    teams: List[ConfigTeam] = []
    teamNumber = 1
    while getenv(f"USER_{userNumber}_TEAM_{teamNumber}"):
        teams.append(parseTeamConfig(teamNumber, userNumber))
        teamNumber += 1
    # Parse other configs of user
    users.append(parseUserConfig(userNumber, teams))
    userNumber += 1

if not users:
    raise MissingConfig("Could not find user private key in config")

##################
# General options
##################

nodeUri = getenv("WEB3_NODE_URI")
reinforceDelayInSeconds = parseInt("REINFORCE_DELAY_IN_SECONDS", 30)
donatePercentage = parsePercentage("DONATE_PERCENTAGE")
donateFrequency = parseInt("DONATE_FREQUENCY", 10)

##################
# Notifications
##################

twilio: Dict[str, Any] = {
    "accountSid": getenv("TWILIO_ACCOUNT_SID"),
    "authToken": getenv("TWILIO_AUTH_TOKEN"),
}

telegram: Dict[str, Any] = {
    "enable": True if "1" == getenv("TELEGRAM_ENABLE", "1") else False,
    "apiKey": getenv("TELEGRAM_API_KEY"),
    "chatId": getenv("TELEGRAM_CHAT_ID"),
}
