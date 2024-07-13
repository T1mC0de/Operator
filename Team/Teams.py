class Team():
    def __init__(self, name, source_logo) -> None:
        self.name = name
        self.source_logo = source_logo

index_first_team = 0
index_second_team = 0

spk = Team (
    "Spartak",
    "../Operator_KHL/Images/logo_spk.png"
)

sev = Team (
    "Severstal",
    "../Operator_KHL/Images/logo_sev.png"
)

Teams_list = [
    spk,
    sev
]