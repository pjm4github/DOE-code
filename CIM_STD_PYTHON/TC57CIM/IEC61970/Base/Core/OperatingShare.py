# Converted by an OPENAI API call using model: gpt-3.5-turbo-1106 on Fri Dec 15 17:03:56 2023
from CIM_STD_PYTHON.TC57CIM.IEC61970.Base.Core.OperatingParticipant import OperatingParticipant


class OperatingShare:
    """
    Specifies the operations contract relationship between a power system resource
    and a contract participant.
    @author kdd
    @version 1.0
    @created 15-Dec-2023 4:38:28 PM
    """

    def __init__(self) -> None:
        """
        Percentage operational ownership between the pair (power system resource 
        and operating participant) associated with this share. The total percentage
        ownership for a power system resource should add to 100%.
        """
        self.percentage = 0
        """
        The operating participant having this share with the associated power system
        resource.
        """
        self.operating_participant: OperatingParticipant = OperatingParticipant()
        """
        The power system resource to which the share applies.
        """
        self.power_system_resource: PowerSystemResource = PowerSystemResource()
